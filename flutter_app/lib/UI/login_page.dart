import 'package:flutter/material.dart';
import 'package:flutter_app/UI/user_page.dart';

//import 'dart:async';
//import 'dart:convert';
//import 'package:http/http.dart' as http;

class Login extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: new ThemeData(primarySwatch: Colors.blue),
      home: new LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  State createState() => new LoginPageState();
}

class LoginPageState extends State<LoginPage>
    with SingleTickerProviderStateMixin {
  Animation<double> _iconAnimation;
  AnimationController _iconAnimationController;

  @override
  void initState() {
    super.initState();
    _iconAnimationController = new AnimationController(
        vsync: this, duration: new Duration(milliseconds: 600));
    _iconAnimation = new CurvedAnimation(
      parent: _iconAnimationController,
      curve: Curves.linear,
    );
    _iconAnimation.addListener(() => this.setState(() {}));
    _iconAnimationController.forward();
  }

  @override
  Widget build(BuildContext context) {

    return new Scaffold(
      backgroundColor: Colors.white,
      body: new Stack(fit: StackFit.expand, children: <Widget>[
        new Image(
          image: new AssetImage("assets/bg.jpg"),
          fit: BoxFit.cover,
          colorBlendMode: BlendMode.darken,
          color: Colors.black87,
        ),
        new Theme(
          data: new ThemeData(
              brightness: Brightness.dark,
              inputDecorationTheme: new InputDecorationTheme(
                // hintStyle: new TextStyle(color: Colors.blue, fontSize: 20.0),
                labelStyle:
                new TextStyle(color: Colors.tealAccent, fontSize: 25.0),
              )),
          isMaterialAppTheme: true,
          child: new Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[

              Center(
                child: Padding(
                  padding: const EdgeInsets.all(10.0),
                  child: Container(
                    decoration: BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage('assets/logo.jpg'),
                        colorFilter: ColorFilter.mode(Colors.greenAccent, BlendMode.darken),
                        fit: BoxFit.fill,
                      ),shape: BoxShape.circle,
                    ),
                    height: _iconAnimation.value * 130.0,
                    width: _iconAnimation.value *  130.0,
                  ),
                ),
              ),
              new Container(
                padding: const EdgeInsets.all(20.0),
                child: new Form(
                  autovalidate: true,
                  child: new Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: <Widget>[
                      new TextFormField(
                        decoration: new InputDecoration(
                            labelText: "Enter Email", fillColor: Colors.white),
                        keyboardType: TextInputType.emailAddress,
                      ),
                      new TextFormField(
                        decoration: new InputDecoration(
                          labelText: "Enter Password",
                        ),
                        obscureText: true,
                        keyboardType: TextInputType.text,
                      ),
                      new Padding(
                        padding: const EdgeInsets.only(top: 25.0),
                      ),
                      new MaterialButton(
                        height: 40.0,
                        minWidth: 150.0,
                        color: Colors.green,
                        splashColor: Colors.amberAccent,
                        textColor: Colors.white,
                        child: new Icon(Icons.arrow_forward_ios),
                        onPressed: () {
                          Navigator.of(context).push(
                              new MaterialPageRoute(builder: (context) => UserPage()));
                        },
                      )
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ]),
    );
  }
}

//Future<Post> fetchPost() async {
//  final response =
//  await http.get('https://jsonplaceholder.typicode.com/posts/1');
//
//  if (response.statusCode == 200) {
//    // If the call to the server was successful, parse the JSON
//    return Post.fromJson(json.decode(response.body));
//  } else {
//    // If that call was not successful, throw an error.
//    throw Exception('Failed to load post');
//  }
//}
//class Post {
//  final String username;
//  final String password;
//
//  Post({this.username, this.password});
//
//
//  factory Post.fromJson(Map<String, dynamic> json) {
//    return Post(
//      username: json['username'],
//      password: json['password'],
//    );
//  }
//}
