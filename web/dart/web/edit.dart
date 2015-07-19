import 'dart:html';
import 'dart:js';

main() {
  querySelector("#renamebtn").onClick.listen((x) {
    var result = context.callMethod('prompt', ['File name']);
    print(result);
    window.location.href =
        "/rename?old=${Uri.encodeComponent(context["FILE_NAME"])}&new=${Uri.encodeComponent(result)}";
  });
}
