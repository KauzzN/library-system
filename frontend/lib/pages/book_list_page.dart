import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class BooksListPage extends StatefulWidget {
  const BooksListPage({super.key});

  @override
  State<BooksListPage> createState() => _BooksListPageState();
}

class _BooksListPageState extends State<BooksListPage> {
  List books = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadBooks();
  }

  Future<void> deleteBook(int id) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("token");

    try {
      final response = await http.delete(
        Uri.parse("http://127.0.0.1:5000/books/delete/$id"),
        headers: {"Authorization": "Bearer $token"},
      );

      print("Status: ${response.statusCode}");
      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              data["mensagem"] ??
                  data["message"] ??
                  "Livro removido com sucesso",
            ),
          ),
        );

        loadBooks();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(data["error"] ?? "Não foi possível remover o livro"),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Erro: $e")));

      print(e);
    }
  }

  Future<void> loadBooks() async {
    try {
      final prefs = await SharedPreferences.getInstance();

      final token = prefs.getString("token");

      final response = await http.get(
        Uri.parse("http://127.0.0.1:5000/books/list"),

        headers: {
          "Authorization": "Bearer $token",
          "Content-Type": "application/json",
        },
      );

      print("Status: ${response.statusCode}");
      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        setState(() {
          books = data;
          loading = false;
        });
      } else {
        setState(() {
          loading = false;
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data["error"] ?? "Erro ao carregar livros")),
        );
      }
    } catch (e) {
      setState(() {
        loading = false;
      });

      print(e);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao conectar ao servidor")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Livros Cadastrados")),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : books.isEmpty
          ? const Center(child: Text("Nenhum livro cadastrado"))
          : ListView.builder(
              padding: const EdgeInsets.all(12),

              itemCount: books.length,

              itemBuilder: (context, index) {
                final book = books[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),

                  child: ListTile(
                    leading: const Icon(Icons.menu_book, color: Colors.indigo),

                    title: Text(book["nome"]),

                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [
                        Text("Categoria: ${book["categoria"]}"),

                        Text("Status: ${book["status"]}"),

                        Text("Estoque: ${book["estoque"]}"),
                      ],
                    ),

                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),

                      onPressed: () {
                        deleteBook(book["id"]);
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}
