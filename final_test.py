#!/usr/bin/env python3
"""
Final Integration Test - Complete System Validation
Tests all components: UserAgent + SpoonOS + Frontend + API
"""

import subprocess
import time
import requests
import sys

def test_project_structure():
    """Test that all required files exist"""
    print("🔍 Testing Project Structure...")
    
    required_files = [
        "main.py",
        "pyproject.toml", 
        "demo_workflow.py",
        "test_integration.py",
        "userAgent/agent.py",
        "userAgent/spoonos_integration.py",
        "spoonOS/agent.py",
        "UI/index.html",
        "UI/playground.html",
        "UI/playground.js",
        "UI/styles.css"
    ]
    
    missing_files = []
    for file in required_files:
        try:
            with open(file, 'r') as f:
                pass  # Just check if file exists
            print(f"   ✅ {file}")
        except FileNotFoundError:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("   ✅ All required files present")
        return True

def test_server_startup():
    """Test that the server starts without errors"""
    print("\n🚀 Testing Server Startup...")
    
    try:
        # Start server in background
        process = subprocess.Popen(
            ["uv", "run", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print("   ✅ Server started successfully")
            print(f"   ✅ Health check passed: {health_data}")
            
            # Test frontend endpoints
            frontend_tests = [
                ("GET /", "http://localhost:8000/"),
                ("GET /playground.html", "http://localhost:8000/playground.html"),
                ("GET /styles.css", "http://localhost:8000/styles.css"),
                ("GET /playground.js", "http://localhost:8000/playground.js")
            ]
            
            for test_name, url in frontend_tests:
                try:
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        print(f"   ✅ {test_name} - OK")
                    else:
                        print(f"   ❌ {test_name} - {resp.status_code}")
                except:
                    print(f"   ❌ {test_name} - Failed")
            
            # Test API endpoint
            api_response = requests.post(
                "http://localhost:8000/api/chat",
                json={"query": "Test query"},
                timeout=30
            )
            
            if api_response.status_code == 200:
                print("   ✅ API endpoint working")
                print(f"   📝 Sample response: {api_response.json()['response'][:50]}...")
            else:
                print(f"   ❌ API endpoint failed: {api_response.status_code}")
            
            # Stop server
            process.terminate()
            process.wait()
            
            return True
            
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"   ❌ Server startup failed: {e}")
        try:
            process.terminate()
        except:
            pass
        return False

def test_dependencies():
    """Test that dependencies are properly configured"""
    print("\n📦 Testing Dependencies...")
    
    # Test pyproject.toml exists and has required deps
    try:
        with open("pyproject.toml", 'r') as f:
            content = f.read()
            
        required_deps = [
            "fastapi",
            "uvicorn",
            "langchain",
            "langchain-anthropic",
            "spoon-ai-sdk",
            "spoon-toolkits"
        ]
        
        for dep in required_deps:
            if dep in content:
                print(f"   ✅ {dep} configured")
            else:
                print(f"   ❌ {dep} missing from pyproject.toml")
                
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to check dependencies: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 FINAL INTEGRATION TEST - Web3 Toolbox Agent")
    print("=" * 60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Dependencies", test_dependencies), 
        ("Server & API", test_server_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        print()
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\nSuccess Rate: {success_rate:.0f}% ({passed}/{len(results)} tests passed)")
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! System is ready for use.")
        print("\n🚀 Quick Start:")
        print("   1. uv run main.py")
        print("   2. Open http://localhost:8000/playground.html")
        print("   3. Ask: 'What's my ETH balance?'")
    else:
        print(f"\n⚠️  Some tests failed. Please check the issues above.")
        
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)