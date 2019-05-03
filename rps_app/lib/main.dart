import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:tflite/tflite.dart';
import 'dart:io';
import 'package:image/image.dart' as ImageFluxer;
import 'package:path_provider/path_provider.dart';
import 'dart:math';

List<CameraDescription> cameras;

void logError(String code, String message) =>
    print('Error: $code\nError Message: $message');

Future<void> main() async {
  try {
    cameras = await availableCameras();
  } on CameraException catch (e) {
    logError(e.code, e.description);
    String res = await _loadModel();
    print(res);
  }
  runApp(MyApp());
}

Future<Null> _loadModel() async {
  try {
    String res = await Tflite.loadModel(
        model: "assets/rps.tflite",
        labels: "assets/labels.txt",
        numThreads: 1); // defaults to 1
    print(res);
  } catch (e) {
    print('Error: $e.code\nError Message: $e.message');
  }
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Camera Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Camera Demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  CameraController _controller;
  String _prediction = "";
  String _random = "";
  String _state = "";

  @override
  void initState() {
    _controller = CameraController(cameras[0], ResolutionPreset.low);
    _controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future appLogic(String filePath) async {
    String res = await Tflite.loadModel(
        model: "assets/rps.tflite",
        labels: "assets/labels.txt",
    );
  
    var recognitions = await Tflite.runModelOnImage(
      path: filePath,
    );

    _prediction = recognitions.elementAt(0)["label"];
    print(_prediction);

    var rng = new Random();
    var guess = rng.nextInt(100);

    if (guess <= 32) {
      _random = "rock";
    } else if (guess > 32 && guess <= 65) {
      _random = "paper";
    } else if (guess > 65 && guess <= 99) {
      _random = "scissors";
    }

    if (_random == "scissors" && _prediction == "paper") {
      _state = "You lose, scissors cuts paper!";
    } else if (_random == "paper" && _prediction == "rock") {
      _state = "You lose, paper covers rock!";
    } else if (_random == "rock" && _prediction == "scissors") {
      _state = "You lose, rock smashes scissors!";
    } else if (_prediction == "scissors" && _random == "paper") {
      _state = "You win, scissors cuts paper!";
    } else if (_prediction == "paper" && _random == "rock") {
      _state = "You win, paper covers rock!";
    } else if (_prediction == "rock" && _random == "scissors") {
      _state = "You win, rock smashes scissors!";
    } else {
      _state = "Draw or unknown";
    }

    setState(() {});
  }

  void _takePicturePressed() {
    takePicture().then((String filePath) {
      if (mounted) {
        print("US" + filePath);
        ImageFluxer.Image img =
            ImageFluxer.decodeImage(new File(filePath).readAsBytesSync());

        ImageFluxer.Image smallImage = ImageFluxer.copyResize(img, 128);
        smallImage = ImageFluxer.normalize(smallImage, 0, 1)

        new File(filePath).writeAsBytesSync(ImageFluxer.encodeJpg(smallImage, {int quality: 100}));
      }
      appLogic(filePath);
    });
  }

  String timestamp() => DateTime.now().millisecondsSinceEpoch.toString();

  Future<String> takePicture() async {
    if (!_controller.value.isInitialized) {
      print("Controller is not initialized");
      return null;
    }

    final Directory extDir = await getApplicationDocumentsDirectory();
    final String dirPath = '${extDir.path}/Pictures/flutter_test';
    await Directory(dirPath).create(recursive: true);
    final String filePath = '$dirPath/${timestamp()}.jpg';

    if (_controller.value.isTakingPicture) {
      // A capture is already pending, do nothing.
      return null;
    }

    try {
      await _controller.takePicture(filePath);
    } on CameraException catch (e) {
      logError(e.code, e.description);
      return null;
    }
    return filePath;
  }

  @override
  Widget build(BuildContext context) {
    if (!_controller.value.isInitialized) {
      return Center(child: Text("Controller is not yet initialized!"));
    }

    return Scaffold(
      body: Center( child: Container( child: Column(
          children: [
            Container(
              margin: const EdgeInsets.all(10.0),
              width: 400.0,
              height: 400.0,
              child: AspectRatio(
                aspectRatio: _controller.value.aspectRatio,
                child: CameraPreview(_controller),
              ),
            ),
            Container(
              child: Expanded(flex: 1, child: Text("You picked: $_prediction")),
            ),
            Container(
              child: Expanded(flex: 1, child: Text("Computer picked: $_random")),
            ),
            Container(
              child: Expanded(flex: 1, child: Text("$_state")),
            ),
          ]
        ),
      ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _takePicturePressed,
        child: const Icon(
          Icons.camera,
          color: Colors.white,
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,

    );
/*
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            AspectRatio(
              aspectRatio: _controller.value.aspectRatio,
              child: CameraPreview(_controller),
            ),
            Padding(
              padding: const EdgeInsets.all(15.0),
              child: Center(
                child: RaisedButton.icon(
                  icon: Icon(Icons.camera),
                  label: Text("Take Picture"),
                  onPressed: _takePicturePressed,
                ),
              ),
            ),
            Expanded(flex: 1, child: Text("You picked: $_prediction")),
            Expanded(flex: 1, child: Text("Computer picked: $_random")),
            Expanded(flex: 1, child: Text("$_state")),
          ],
        ),
      ),
    );*/
  }
}
