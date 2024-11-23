import 'package:flutter/material.dart';

class ProfileSetupScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Profile')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            CircleAvatar(radius: 50, child: Icon(Icons.camera_alt, size: 30)),
            SizedBox(height: 16),
            ProfileInputField(label: 'Full Name'),
            SizedBox(height: 16),
            ProfileInputField(label: 'Your mobile number'),
            SizedBox(height: 16),
            ProfileInputField(label: 'Email'),
            SizedBox(height: 16),
            ProfileInputField(label: 'City'),
            SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () {},
                    child: Text('Cancel'),
                  ),
                ),
                SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {},
                    child: Text('Save'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class ProfileInputField extends StatelessWidget {
  final String label;

  ProfileInputField({required this.label});

  @override
  Widget build(BuildContext context) {
    return TextField(
      decoration: InputDecoration(labelText: label),
    );
  }
}
