# Python Upgrade Guide

## Current Situation

- **Current Python**: 3.7.4
- **Required for google-generativeai**: Python 3.9+
- **Recommended**: Python 3.10 or 3.11 (best compatibility)

## Quick Upgrade Options

### Option 1: Official Python Installer (Recommended)

1. **Download Python 3.11** (or latest stable):
   - Visit: https://www.python.org/downloads/
   - Download Windows installer (64-bit recommended)

2. **Install**:
   - ✅ Check "Add Python to PATH" (important!)
   - ✅ Check "Install for all users" (optional)
   - Click "Install Now"

3. **Verify**:
   ```powershell
   python --version
   # Should show Python 3.11.x or higher
   ```

4. **Reinstall packages**:
   ```powershell
   pip install -r requirements.txt
   ```

### Option 2: Using py Launcher (Windows)

If you have multiple Python versions:

```powershell
# Install Python 3.11
py -3.11 -m pip install --upgrade pip

# Use specific version
py -3.11 discord_bot.py
```

### Option 3: Virtual Environment (Recommended for Projects)

```powershell
# Create new venv with Python 3.11
py -3.11 -m venv myEnv

# Activate
.\myEnv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

## After Upgrading

1. **Verify Python version**:
   ```powershell
   python --version
   ```

2. **Install Gemini SDK**:
   ```powershell
   pip install google-generativeai
   ```

3. **Test**:
   ```powershell
   python scripts/test_gemini.py
   ```

## Notes

- Your existing `myEnv` virtual environment is Python 3.7
- You may want to create a new venv with Python 3.11
- Or upgrade the existing one (though creating new is cleaner)

## Quick Commands

```powershell
# Check current version
python --version

# After upgrade, verify
python --version

# Install all requirements
pip install -r requirements.txt

# Test Gemini
python scripts/test_gemini.py
```

