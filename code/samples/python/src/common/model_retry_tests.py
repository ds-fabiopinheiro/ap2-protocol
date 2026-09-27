# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for common.model_retry against a simulated Gemini API."""

import asyncio
import json
import time

import httpx
import pytest

from google import genai
from google.genai import errors
from google.genai import types

from common import model_retry

_MODEL = "gemini-3.1-flash-lite-preview"

_OK_BODY = {
    "candidates": [{
        "content": {"role": "model", "parts": [{"text": "ok"}]},
        "finishReason": "STOP",
    }]
}


def _error_body(code: int, status: str) -> dict:
  return {"error": {"code": code, "message": status, "status": status}}


class _FakeGemini:
  """Answers with the queued responses and records the call times."""

  def __init__(self, responses):
    self._responses = list(responses)
    self.call_times = []

  def handler(self, request: httpx.Request) -> httpx.Response:
    self.call_times.append(time.monotonic())
    status, body, headers = self._responses.pop(0)
    return httpx.Response(
        status, content=json.dumps(body), headers=headers or {}
    )


def _call(fake: _FakeGemini):
  client = genai.Client(
      api_key="test-key",
      http_options=types.HttpOptions(
          retry_options=model_retry.gemini_retry_options(),
          async_client_args={"transport": httpx.MockTransport(fake.handler)},
      ),
  )
  return asyncio.run(
      client.aio.models.generate_content(model=_MODEL, contents="hi")
  )


def test_retries_503_then_succeeds_with_growing_waits():
  fake = _FakeGemini([
      (503, _error_body(503, "UNAVAILABLE"), None),
      (503, _error_body(503, "UNAVAILABLE"), None),
      (200, _OK_BODY, None),
  ])
  response = _call(fake)
  assert response.text == "ok"
  assert len(fake.call_times) == 3
  first_wait = fake.call_times[1] - fake.call_times[0]
  second_wait = fake.call_times[2] - fake.call_times[1]
  # 2 s and 4 s plus up to 1 s of jitter.
  assert 2.0 <= first_wait < 3.5
  assert 4.0 <= second_wait < 5.5


def test_gives_up_after_two_retries():
  fake = _FakeGemini([(503, _error_body(503, "UNAVAILABLE"), None)] * 4)
  with pytest.raises(errors.ServerError) as exc_info:
    _call(fake)
  assert exc_info.value.code == 503
  assert len(fake.call_times) == 3


@pytest.mark.parametrize(
    "status,name,headers",
    [
        (429, "RESOURCE_EXHAUSTED", {"Retry-After": "1"}),
        (429, "RESOURCE_EXHAUSTED", None),
        (400, "INVALID_ARGUMENT", None),
        (500, "INTERNAL", None),
    ],
)
def test_does_not_retry_other_errors(status, name, headers):
  fake = _FakeGemini([(status, _error_body(status, name), headers)] * 2)
  with pytest.raises(errors.APIError) as exc_info:
    _call(fake)
  assert exc_info.value.code == status
  assert len(fake.call_times) == 1


def test_adk_gemini_model_retries_503():
  from google.adk.models.google_llm import Gemini  # pylint: disable=g-import-not-at-top
  from google.adk.models.llm_request import LlmRequest  # pylint: disable=g-import-not-at-top

  fake = _FakeGemini([
      (503, _error_body(503, "UNAVAILABLE"), None),
      (200, _OK_BODY, None),
  ])
  llm = Gemini(model=_MODEL, retry_options=model_retry.gemini_retry_options())
  # Same client ADK builds in Gemini.api_client, with the fake transport.
  llm.__dict__["api_client"] = genai.Client(
      api_key="test-key",
      http_options=types.HttpOptions(
          retry_options=llm.retry_options,
          async_client_args={"transport": httpx.MockTransport(fake.handler)},
      ),
  )
  request = LlmRequest(
      model=_MODEL,
      contents=[types.Content(role="user", parts=[types.Part(text="hi")])],
  )

  async def run():
    return [r async for r in llm.generate_content_async(request)]

  responses = asyncio.run(run())
  assert responses[-1].content.parts[0].text == "ok"
  assert len(fake.call_times) == 2
