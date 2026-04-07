# Spam Detection Agent - Testing Guide

## Test Suite Overview

The project includes comprehensive unit tests for:
1. **spam_classifier.py** - Transcript classification and evidence extraction
2. **telegram_notifier.py** - Telegram alert formatting and sending
3. **agent.py** - Core agent functionality (transcript extraction, config)

## Test Files Location

All tests are in the `tests/` directory:
- `tests/test_spam_classifier.py` - Tests for spam classification
- `tests/test_telegram_notifier.py` - Tests for Telegram notifications
- `tests/test_agent.py` - Tests for agent core functionality
- `tests/conftest.py` - Test configuration

## How to Run Tests

### Install Test Dependencies
```bash
uv sync --extra test
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Files
```bash
python -m pytest tests/test_spam_classifier.py -v
python -m pytest tests/test_telegram_notifier.py -v
python -m pytest tests/test_agent.py -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/ --cov=spam_classifier --cov=telegram_notifier --cov=agent
```

## What Is Tested

### Spam Classifier Tests
- Empty and whitespace-only transcripts
- Spam classification with mocked OpenAI responses
- Legitimate classification with mocked OpenAI responses
- Error handling when OpenAI API fails

### Telegram Notifier Tests
- HTML escaping of special characters
- Message formatting for spam calls
- Message formatting for legitimate calls
- Message building when no evidence is present
- HTML message formatting
- Handling missing Telegram credentials
- Successful alert sending
- HTTP error handling during alert sending

### Agent Tests
- Transcript extraction from chat context (various scenarios)
- SpamDetectionConfig default and custom values
- VoiceAgent initialization
- Filtering of empty/whitespace-only messages

## Testing Frequency Recommendations

### Development Phase
- **Run tests after every change**: `python -m pytest tests/ -x`
- **Run full test suite before commits**: Ensures nothing is broken
- **Test when adding new features**: Write tests first (TDD approach)

### Pre-Deployment
- **Run full test suite**: `python -m pytest tests/ --tb=short`
- **Run with coverage**: Ensure >80% coverage
- **Test edge cases**: Empty transcripts, malformed data, network failures

### Continuous Integration (When Ready)
- **On every push**: Run unit tests
- **On pull requests**: Run full test suite + coverage check
- **Nightly**: Run extended tests if any are added

## Writing New Tests

### Guidelines
1. **Follow AAA pattern**: Arrange, Act, Assert
2. **Test one thing per test**: Keep tests focused
3. **Use descriptive names**: `test_what_when_then_expected`
4. **Mock external dependencies**: Don't test OpenAI/Telegram directly
5. **Test edge cases**: Empty inputs, boundary values, error conditions

### Example Test Structure
```python
@pytest.mark.asyncio
async def test_your_function_scenario_expected_behavior():
    # Arrange - Set up test data and mocks
    test_input = "..."
    with patch('dependency.to.mock') as mock:
        mock.return_value = AsyncMock(return_value=expected_result)
        
        # Act - Call the function
        result = await your_function(test_input)
        
        # Assert - Verify the outcome
        assert result == expected
        # Additional assertions as needed
```

## Test Data Examples

Use these transcript examples in your tests:

**Spam Indicators:**
- "I'm calling from Windows Tech Support about a virus on your computer"
- "You've won a free cruise! Just provide your credit card to cover taxes"
- "This is your bank calling about suspicious activity on your account"
- "Limited time offer! Act now to get 50% off life insurance"

**Legitimate Calls:**
- "Hi, this is Sarah from next door. I found your dog in my yard"
- "This is Dr. Lee's office calling to confirm your appointment tomorrow"
- "Hi, I'm calling about the item you listed on Craigslist"
- "This is your child's school nurse. They scraped their knee at recess"

## Common Testing Patterns

### Mocking OpenAI Responses
```python
with patch('spam_classifier.AsyncOpenAI') as mock_openai_class:
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        result = await classify_transcript(transcript)
```

### Mocking HTTP Requests (Telegram)
```python
mock_response = AsyncMock()
mock_response.raise_for_status = AsyncMock()

mock_client = AsyncMock()
mock_client.__aenter__.return_value.post = AsyncMock(return_value=mock_response)

with patch('telegram_notifier.httpx.AsyncClient', return_value=mock_client):
    # Test code here
```

## Troubleshooting Tests

### "ModuleNotFoundError: No module named 'livekit'"
- The agent tests mock LiveKit dependencies
- This is expected and handled in test_agent.py
- If you see this elsewhere, check your imports

### Async test issues
- Ensure test methods are marked with `@pytest.mark.asyncio`
- Use `AsyncMock` for asynchronous mocks
- Remember to `await` asynchronous function calls

### Environment variable issues
- Tests use `patch.dict(os.environ, {...})` to set required vars
- Remember to restore environment after tests (patch handles this automatically)

## Next Steps for Testing

1. **Add integration tests**: Test the full pipeline with LiveKit rooms
2. **Add end-to-end tests**: Simulate actual calls from start to Telegram alert
3. **Performance tests**: Measure classification speed, memory usage
4. **Chaos testing**: Test behavior under network failures, high load
5. **Property-based testing**: Use hypothesis for edge case discovery

The current test suite provides solid coverage for the core logic and helps prevent regressions as you develop the spam detection agent further.