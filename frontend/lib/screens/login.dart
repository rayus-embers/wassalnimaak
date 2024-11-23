import 'package:flutter/material.dart';

import 'profile_setup.dart';
import 'set_password.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ProfileInputField(label: 'Enter your email'),
            SizedBox(height: 16),
            PasswordInputField(label: 'Password'),
            SizedBox(height: 8),
            TextButton(
              onPressed: () {},
              child: Text('Forgot Password?'),
            ),
            SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {},
              child: Text('Log In'),
            ),
          ],
        ),
      ),
    );
  }
}
