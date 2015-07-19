import 'dart:html';
import 'dart:js';

main() {
  querySelector("#newfilebtn").onClick.listen((x) {
    var result = context.callMethod('prompt', ['File name']);
    print(result);
    window.location.href = "/newfile?name=${Uri.encodeComponent(result)}";
  });
}
