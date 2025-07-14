import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';
// import 'dart:io';
// import 'package:multicast_dns/multicast_dns.dart';
import 'dart:developer' as developer;


void main() {
  // testLocalNetwork();
  // triggerBonjourDiscovery();

  // Enable VM service
  developer.Service.controlWebServer(enable: true);

  enableFlutterDriverExtension();
  runApp(const MyApp());
}

// void testLocalNetwork() async {
//   try {
//     // محاولة فتح socket على شبكة محلية (ليس localhost)
//     final socket = await Socket.connect('192.168.1.1', 80, timeout: Duration(seconds: 2));
//     socket.destroy();
//   } catch (_) {
//     debugPrint("Local network test completed");
//   }
// }

// void triggerBonjourDiscovery() async {
//   final mdns = MDnsClient();
//   await mdns.start();
//   // نعمل بحث عن أي service وهمية
//   await for (final PtrResourceRecord ptr in mdns.lookup<PtrResourceRecord>(
//     ResourceRecordQuery.serverPointer('_http._tcp.local'),
//   )) {
//     break; // بمجرد يحصل بحث، macOS يطلب الصلاحية
//   }
//   mdns.stop();
// }


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login App POC',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();

  bool _isLoading = false;
  String? _emailError;
  String? _phoneError;
  String? _passwordError;
  
  @override
  void dispose() {
    _phoneController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    setState(() {
      _emailError = null;
      _phoneError = null;
      _passwordError = null;
    });

    final email = _emailController.text.trim();
    final phone = _phoneController.text.trim();
    final password = _passwordController.text;
    
    bool hasError = false;

    if (email.isEmpty) {
      setState(() {
        _emailError = 'Please enter your email';
      });
      hasError = true;
    } else if (!RegExp(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$").hasMatch(email)) {
      setState(() {
        _emailError = 'Invalid email';
      });
      hasError = true;
    }

    if (phone.isEmpty) {
      setState(() {
        _phoneError = 'Please enter your phone number';
      });
      hasError = true;
    } else if (phone.length < 10) {
      setState(() {
        _phoneError = 'Phone number must be at least 10 digits';
      });
      hasError = true;
    }
   
    if (password.isEmpty) {
      setState(() {
        _passwordError = 'Please enter your password';
      });
      hasError = true;
    } else if (password.length < 6) {
      setState(() {
        _passwordError = 'Password must be at least 6 characters';
      });
      hasError = true;
    }

    if (hasError) return;

    setState(() {
      _isLoading = true;
    });

    await Future.delayed(const Duration(seconds: 5));

    setState(() {
      _isLoading = false;
    });

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Success Login!")));
    }

    // if (mounted) {
    //   Navigator.of(context).push(
    //     MaterialPageRoute(builder: (context) => const SuccessScreen()),
    //   );
    // }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              
              /// welcome text
              const Text(
                'Welcome',
                key: Key('welcome_text'),
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                ),
              ),
              
              const SizedBox(height: 40),

              /// email field
              TextFormField(
                key: const Key('email_field'),
                controller: _emailController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'Enter your email',
                  prefixIcon: Icon(Icons.phone),
                  border: OutlineInputBorder(),
                ),
                // No validator here
              ),
              if (_emailError != null)
                Padding(
                  padding: const EdgeInsets.only(top: 4.0),
                  child: Text(
                    _emailError!,
                    key: const Key('email_validation_error'),
                    style: const TextStyle(color: Colors.red, fontSize: 14),
                  ),
                ),
              
              const SizedBox(height: 16),
              

              /// phone field
              TextFormField(
                key: const Key('phone_field'),
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  labelText: 'Phone Number',
                  hintText: 'Enter your phone number',
                  prefixIcon: Icon(Icons.phone),
                  border: OutlineInputBorder(),
                ),
                // No validator here
              ),
              if (_phoneError != null)
                Padding(
                  padding: const EdgeInsets.only(top: 4.0),
                  child: Text(
                    _phoneError!,
                    key: const Key('phone_validation_error'),
                    style: const TextStyle(color: Colors.red, fontSize: 14),
                  ),
                ),
              
              const SizedBox(height: 16),
              
              /// password field
              TextFormField(
                key: const Key('password_field'),
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  hintText: 'Enter your password',
                  prefixIcon: Icon(Icons.lock),
                  border: OutlineInputBorder(),
                ),
                // No validator here
              ),
              if (_passwordError != null)
                Padding(
                  padding: const EdgeInsets.only(top: 4.0),
                  child: Text(
                    _passwordError!,
                    key: const Key('password_validation_error'),
                    style: const TextStyle(color: Colors.red, fontSize: 14),
                  ),
                ),
             
              const SizedBox(height: 24),
             
              /// login button
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  key: const Key('login_button'),
                  onPressed: _isLoading ? null : _handleLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(
                          color: Colors.white,
                          key: Key('loading_indicator'),
                        )
                      : const Text(
                          'Login',
                          style: TextStyle(fontSize: 16),
                        ),
                ),
              ),

            ],
          ),
        ),
      ),
    );
  }
}

//
// class SuccessScreen extends StatelessWidget {
//   const SuccessScreen({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text('Success'),
//         backgroundColor: Theme.of(context).colorScheme.inversePrimary,
//       ),
//       body: const Center(
//         child: Text(
//           'Login Successful!',
//           key: Key('success_text'),
//           style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
//         ),
//       ),
//     );
//   }
// }
