import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:appium_testing_poc/main.dart';

void main() {

  group('LoginScreen Widget Tests', () {

    testWidgets('Shows error if fields are empty', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      // Tap login without entering anything
      final loginButton = find.byKey(const Key('login_button'));
      await tester.tap(loginButton);
      await tester.pump(); // Rebuild after tap

      expect(find.text('Please enter your email'), findsOneWidget);
      expect(find.text('Please enter your phone number'), findsOneWidget);
      expect(find.text('Please enter your password'), findsOneWidget);
    });

    testWidgets('Shows error for invalid email and short phone/password', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      await tester.enterText(find.byKey(const Key('email_field')), 'invalid');
      await tester.enterText(find.byKey(const Key('phone_field')), '123');
      await tester.enterText(find.byKey(const Key('password_field')), '123');
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pump();

      expect(find.text('Invalid email'), findsOneWidget);
      expect(find.text('Phone number must be at least 10 digits'), findsOneWidget);
      expect(find.text('Password must be at least 6 characters'), findsOneWidget);
    });

    testWidgets('show error when invalid email entered while coorect email & password entered', (WidgetTester tester) async {
      await tester.pumpWidget(MaterialApp(home: LoginScreen()));

      await tester.enterText(find.byType(TextFormField).at(0), 'belal.nayzak');
      await tester.enterText(find.byType(TextFormField).at(1), '01102288599');
      await tester.enterText(find.byType(TextFormField).at(2), 'Password123');
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pump(); // Rebuild after tap

      expect(find.text('Invalid email'), findsOneWidget);
    });

    testWidgets('Shows success snackbar on valid input', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());

      await tester.enterText(find.byKey(const Key('email_field')), 'test@example.com');
      await tester.enterText(find.byKey(const Key('phone_field')), '1234567890');
      await tester.enterText(find.byKey(const Key('password_field')), '123456');
      await tester.tap(find.byKey(const Key('login_button')));

      // Wait for loading indicator to disappear (5 seconds)
      await tester.pump(const Duration(seconds: 5));
      await tester.pump(); // Rebuild after loading

      expect(find.text('Success Login!'), findsOneWidget);
    });
  });
}