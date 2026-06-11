import 'package:flutter/material.dart';
import 'package:library_system_mobile/pages/book_page.dart';
import 'package:library_system_mobile/pages/loan_page.dart';
import 'package:library_system_mobile/pages/login_page.dart';
import 'package:library_system_mobile/pages/book_list_page.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:library_system_mobile/pages/loans-list_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  Future<void> logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.remove("token");

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Biblioteca Digital"),
        centerTitle: true,
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            SizedBox(
              width: double.infinity,
              height: 60,

              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const BooksListPage()),
                  );
                },

                icon: const Icon(Icons.library_books),

                label: const Text("Listar Livros"),
              ),
            ),

            const SizedBox(height: 16),

            SizedBox(
              width: double.infinity,
              height: 60,

              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CreateBookPage()),
                  );
                },

                icon: const Icon(Icons.menu_book),
                label: const Text("Livros"),
              ),
            ),

            const SizedBox(height: 16),

            SizedBox(
              width: double.infinity,
              height: 60,

              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const LoansPage()),
                  );
                },

                icon: const Icon(Icons.handshake),
                label: const Text("Listar empréstimos"),
              ),
            ),

            const SizedBox(height: 16),

            SizedBox(
              width: double.infinity,
              height: 60,

              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const LoanPage()),
                  );
                },

                icon: const Icon(Icons.handshake),
                label: const Text("Empréstimos"),
              ),
            ),

            const Spacer(),

            SizedBox(
              width: double.infinity,
              height: 60,

              child: ElevatedButton.icon(
                onPressed: () {
                  logout(context);
                },

                icon: const Icon(Icons.logout),
                label: const Text("Logout"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
