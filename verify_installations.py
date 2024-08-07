try:
    import flask
    print("Flask installed successfully")
except ImportError:
    print("Flask not installed")

try:
    import bcrypt
    print("bcrypt installed successfully")
except ImportError:
    print("bcrypt not installed")

try:
    import stegano
    print("Stegano installed successfully")
except ImportError:
    print("Stegano not installed")

try:
    import cryptosteganography
    print("Cryptosteganography installed successfully")
except ImportError:
    print("Cryptosteganography not installed")

try:
    import unittest
    print("unittest installed successfully (part of the standard library)")
except ImportError:
    print("unittest not installed")

try:
    import pytest
    print("pytest installed successfully")
except ImportError:
    print("pytest not installed")

try:
    import locust
    print("locust installed successfully")
except ImportError:
    print("locust not installed")

try:
    import bandit
    print("bandit installed successfully")
except ImportError:
    print("bandit not installed")

try:
    import pylint
    print("pylint installed successfully")
except ImportError:
    print("pylint not installed")
