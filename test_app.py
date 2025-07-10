#!/usr/bin/env python3
"""
Test script for Support Squad Backend

This script tests the main endpoints of the FastAPI application
to ensure everything is working correctly.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_CONVERSATION_ID = f"test-conv-{int(time.time())}"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def test_direct_message():
    """Test the direct message processing endpoint"""
    print("\nTesting direct message endpoint...")
    try:
        payload = {
            "message": "Hello, I need help with my order",
            "conversation_id": TEST_CONVERSATION_ID
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/message",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Direct message endpoint working")
            result = response.json()
            print(f"   Response: {result['response']}")
            print(f"   Conversation ID: {result['conversation_id']}")
        else:
            print(f"❌ Direct message endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Direct message endpoint error: {e}")

def test_chatwoot_webhook():
    """Test the Chatwoot webhook endpoint"""
    print("\nTesting Chatwoot webhook endpoint...")
    try:
        # Test with simple format
        payload = {
            "message": "I have a technical issue that needs support",
            "conversation_id": f"chatwoot-{TEST_CONVERSATION_ID}",
            "sender_id": "user-123",
            "account_id": "account-789"
        }
        
        response = requests.post(
            f"{BASE_URL}/chatwoot/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Chatwoot webhook endpoint working (simple format)")
            result = response.json()
            print(f"   Response: {result['response']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Chatwoot webhook endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Chatwoot webhook endpoint error: {e}")

def test_chatwoot_webhook_complex():
    """Test the Chatwoot webhook with complex format"""
    print("\nTesting Chatwoot webhook with complex format...")
    try:
        # Test with Chatwoot format
        payload = {
            "conversation": {
                "id": f"chatwoot-complex-{TEST_CONVERSATION_ID}",
                "account_id": "account-789",
                "messages": [
                    {
                        "content": "Can you help me with my purchase?",
                        "sender_id": "user-456"
                    }
                ]
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/chatwoot/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Chatwoot webhook endpoint working (complex format)")
            result = response.json()
            print(f"   Response: {result['response']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Chatwoot webhook endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Chatwoot webhook endpoint error: {e}")

def test_conversation_history():
    """Test the conversation history endpoint"""
    print("\nTesting conversation history endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/conversations/{TEST_CONVERSATION_ID}/history")
        
        if response.status_code == 200:
            print("✅ Conversation history endpoint working")
            result = response.json()
            print(f"   Conversation ID: {result['conversation_id']}")
            print(f"   History entries: {len(result['history'])}")
        else:
            print(f"❌ Conversation history endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Conversation history endpoint error: {e}")

def test_mock_responses():
    """Test various mock responses from the ADK"""
    print("\nTesting various mock responses...")
    
    test_messages = [
        "Hello there!",
        "I need help with support",
        "What's the weather like?",
        "I have an order issue",
        "Goodbye and thank you"
    ]
    
    for message in test_messages:
        try:
            payload = {
                "message": message,
                "conversation_id": f"mock-test-{int(time.time())}"
            }
            
            response = requests.post(
                f"{BASE_URL}/chat/message",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ '{message}' → '{result['response'][:50]}...'")
            else:
                print(f"❌ Failed to process: {message}")
        except Exception as e:
            print(f"❌ Error processing '{message}': {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Support Squad Backend Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            print("   Make sure the FastAPI server is running on http://localhost:8000")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
        print("   Run: python main.py")
        return
    
    # Run tests
    test_health_endpoint()
    test_root_endpoint()
    test_direct_message()
    test_chatwoot_webhook()
    test_chatwoot_webhook_complex()
    test_conversation_history()
    test_mock_responses()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Check the interactive API docs at: http://localhost:8000/docs")
    print("2. Configure Chatwoot webhook to point to: http://localhost:8000/chatwoot/webhook")
    print("3. Test with real Chatwoot messages")

if __name__ == "__main__":
    main() 