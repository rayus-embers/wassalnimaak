import 'package:flutter/material.dart';
import 'screens/signup.dart';
import 'screens/phone_verification.dart';
import 'screens/set_password.dart';
import 'screens/profile_setup.dart';
import 'screens/login.dart';
import 'screens/welcome.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Waggalni Maak',
      theme: ThemeData(
        primaryColor: const Color(0xFFFF5C5C),
        hintColor: const Color(0xFFFF5C5C),
        textTheme: TextTheme(
          headline1: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.black),
          bodyText1: TextStyle(fontSize: 16, color: Colors.black),
          bodyText2: TextStyle(fontSize: 14, color: Color(0xFF8A8A8A)),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFFF8F8F8),
          contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: Color(0xFFB8B8B8)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: Color(0xFFFF5C5C), width: 2),
          ),
          hintStyle: const TextStyle(color: Color(0xFFB8B8B8)),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFFFF5C5C),
            minimumSize: const Size(double.infinity, 50),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
        ),
      ),
      initialRoute: '/signup',
      routes: {

        '/signup': (context) => SignUpScreen(),
        '/welcome': (context) => WelcomeScreen(),
        '/phoneVerification': (context) => PhoneVerificationScreen(),
        '/setPassword': (context) => SetPasswordScreen(),
        '/profileSetup': (context) => ProfileSetupScreen(),
        '/login': (context) => LoginScreen(),
      },
    );
  }
}
