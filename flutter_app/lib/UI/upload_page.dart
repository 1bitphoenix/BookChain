import 'package:flutter/material.dart';
import 'package:flutter_webview_plugin/flutter_webview_plugin.dart';

class UploadPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Upload Book',
      routes: {
        "/": (_) => new WebviewScaffold(
          url: "https://piyush.tech/books",
          appBar: new AppBar(
            title: new Text("Upload Book"),
          ),
        )
      },
    );
  }
}