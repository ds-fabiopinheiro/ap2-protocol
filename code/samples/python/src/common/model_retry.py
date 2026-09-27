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

"""Retry settings for calls to the Gemini API.

The retry happens inside the google-genai HTTP client, so only the model
request is repeated: tool calls and the rest of the agent turn are not.
"""

from google.genai import types

# 503 UNAVAILABLE ("model overloaded") is the only status retried. 429 is not:
# the client waits a fixed backoff and ignores Retry-After / RetryInfo, so a
# retry would spend more of the free-tier quota (15 RPM) and fail again.
# 400 and other client errors are never retried.
RETRYABLE_STATUS_CODES = (503,)

# Original request + 2 retries.
MAX_ATTEMPTS = 3

# Waits grow as 2 s, 4 s (plus up to 1 s of jitter), capped at 8 s.
INITIAL_DELAY_SECONDS = 2.0
MAX_DELAY_SECONDS = 8.0
EXP_BASE = 2.0
JITTER_SECONDS = 1.0


def gemini_retry_options() -> types.HttpRetryOptions:
  """Returns the retry options for the native Gemini client."""
  return types.HttpRetryOptions(
      attempts=MAX_ATTEMPTS,
      initial_delay=INITIAL_DELAY_SECONDS,
      max_delay=MAX_DELAY_SECONDS,
      exp_base=EXP_BASE,
      jitter=JITTER_SECONDS,
      http_status_codes=list(RETRYABLE_STATUS_CODES),
  )
