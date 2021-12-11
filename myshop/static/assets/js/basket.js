let elements = document.querySelectorAll("div.product-quantity");
 for (let elem of elements) {
    elem.addEventListener('input', function (e) {

    elem.querySelector("input[type=submit]").click();
    //console.log("input event detected! coming from this element:", e.target);
}, false);
  }