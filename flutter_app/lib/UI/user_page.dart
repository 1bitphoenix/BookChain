import 'package:flutter/material.dart';
import 'package:flutter_app/UI/search_page.dart';
import 'package:flutter_app/UI/upload_page.dart';
import 'package:flutter_app/UI/user_profile_page.dart';

class UserPage extends StatelessWidget{
  @override
  Widget build(BuildContext context) {
   return MaterialApp(
     debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Container(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: GestureDetector(
                    onTap: (){
                      Navigator.of(context).push(MaterialPageRoute(builder: (context) => UserProfile()));
                    },
                    child: Container(
                      decoration: BoxDecoration(
                        image: DecorationImage(
                          image: AssetImage('assets/propic.jpeg'),
                          fit: BoxFit.fill,
                        ),
                        shape: BoxShape.circle,
                      ),
                      height: 140.0,
                      width: 140.0,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: MaterialButton(
                    onPressed: (){
                      Navigator.of(context).push(
                          MaterialPageRoute(builder: (context) => UploadPage())
                      );
                    },
                    height: 70.0,
                    minWidth: 170.0,
                    splashColor: Colors.tealAccent,
                    textColor: Colors.white,
                    color: Colors.teal,
                    child: Text('Upload Book', textScaleFactor: 2.0,),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: MaterialButton(
                    onPressed: (){
                      Navigator.of(context).push(MaterialPageRoute(builder: (context) => SearchPage()));
                    },
                    height: 70.0,
                    minWidth: 170.0,
                    textColor: Colors.white,
                    color: Colors.teal,
                    splashColor: Colors.tealAccent,
                    child: Text('Search Book', textScaleFactor: 2.0,),
                  ),
                )
              ],
            ),
          ),
        ),
      ),
   );
  }
}