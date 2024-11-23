import 'package:flutter/material.dart';

class SetPasswordScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Set Password')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            PasswordInputField(label: 'Enter Your Password'),
            SizedBox(height: 16),
            PasswordInputField(label: 'Confirm Password'),
            SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {},
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

class PasswordInputField extends StatelessWidget {
  final String label;

  PasswordInputField({required this.label});

  @override
  Widget build(BuildContext context) {
    return TextField(
      obscureText: true,
      decoration: InputDecoration(labelText: label),
    );
  }
}
