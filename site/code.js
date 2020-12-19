var canvas, ctx, mouseOverCanvas, mouseOverSlider;
var width, height, radius, x_orig, y_orig;


window.addEventListener("load", () => {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    resize();
    document.addEventListener("mousedown", startDrawing);
    document.addEventListener("mouseup", stopDrawing);
    document.addEventListener("mousemove", Draw);
  
    document.addEventListener("touchstart", startDrawing);
    document.addEventListener("touchend", stopDrawing);
    document.addEventListener("touchcancel", stopDrawing);
    document.addEventListener("touchmove", Draw);
    window.addEventListener("resize", resize);
  
    document.getElementById("x_coordinate").innerText = 0;
    document.getElementById("y_coordinate").innerText = 0;
  });

function background() {
  x_orig = width / 2;
  y_orig = height * 1.8;

  ctx.beginPath();
  ctx.arc(x_orig, y_orig, radius - 60, 0, Math.PI * 2, true);
  ctx.fillStyle = "#383838";
  ctx.fill();
}

function joystick(width, height) {
  ctx.beginPath();
  ctx.arc(width, height, radius, 0, Math.PI * 2, true);
  ctx.fillStyle = "#333333";
  ctx.fill();
  ctx.strokeStyle = "#575757";
  ctx.lineWidth = 10;
  ctx.stroke();
}

function resize() {
  radius = 180; // specify the radius to 180
  width = window.innerWidth; //Sets the variable width to be equal to the windows width
  height = radius + 25; //Sets the variable height
  ctx.canvas.width = width; //sets the canvas width to be equal to variable width
  ctx.canvas.height = 800; //sets the canvas height
  background(); //draw the background
  joystick(width / 2, height * 1.8); //sends to the joystick function this variables
}

let coord = { x: 0, y: 0 };
let paint = false;

function getPosition(event) {
  var mouse_x = event.clientX || event.touches[0].clientX;
  var mouse_y = event.clientY || event.touches[0].clientY;

  coord.x = (mouse_x - canvas.offsetLeft) * 1.43;
  coord.y = (mouse_y - canvas.offsetTop) * 1.43;
}

function is_it_in_the_circle() {
  var current_radius = Math.sqrt(
    Math.pow(coord.x - x_orig, 2) + Math.pow(coord.y - y_orig, 2)
  );
  if (radius >= current_radius) return true;
  else return false;
}

function startDrawing(event) {
  if (mouseOverCanvas) {
    paint = true;
    getPosition(event);
    if (is_it_in_the_circle()) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      background();
      joystick(coord.x, coord.y);
      Draw(event);
    }
  }
}

function Draw(event) {
  if (paint) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background();
    var angle_in_degrees, x, y, speed;
    var angle = Math.atan2(coord.y - y_orig, coord.x - x_orig);

    if (Math.sign(angle) == -1) {
      angle_in_degrees = Math.round((-angle * 180) / Math.PI);
    } else {
      angle_in_degrees = Math.round(360 - (angle * 180) / Math.PI);
    }

    if (is_it_in_the_circle()) {
      joystick(coord.x, coord.y);
      x = coord.x;
      y = coord.y;
    } else {
      x = radius * Math.cos(angle) + x_orig;
      y = radius * Math.sin(angle) + y_orig;
      joystick(x, y);
    }

    getPosition(event);

    var speed = Math.round(
      (100 * Math.sqrt(Math.pow(x - x_orig, 2) + Math.pow(y - y_orig, 2))) /
        radius
    );
    var x_relative = Math.round(x - x_orig);
    var y_relative = Math.round(y - y_orig) * -1;

    document.getElementById("x_coordinate").innerText = x_relative;
    document.getElementById("y_coordinate").innerText = y_relative;

    a1 = document.getElementById("slider1").value;
    a2 = document.getElementById("slider2").value;

    httpGet(
      "api?x=" +
        x_relative +
        "&y=" +
        y_relative +
        "&a1=" +
        a1 +
        "&maxSpeed=" +
        a2,
      false
    );
  }
}

async function stopDrawing() {
  paint = false;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  background();
  joystick(width / 2, height * 1.8);
  document.getElementById("slider1").value = 0;
  document.getElementById("x_coordinate").innerText = 0;
  document.getElementById("y_coordinate").innerText = 0;
  await sleep(60);
  var a = document.getElementById("slider2").value;
  httpGet("api?x=" + 0 + "&y=" + 0 + "&a1=" + 0 + "&maxSpeed=" + a, true);
  httpGet("api?x=" + 0 + "&y=" + 0 + "&a1=" + 0 + "&maxSpeed=" + a, true);
}

var oldTime = 0;

function httpGet(theUrl, ignoreTimeout) {
  time = new Date();
  if (oldTime + 100 <= time.getTime() || ignoreTimeout) {
    console.log(theUrl);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, true); // false for synchronous request
    xmlHttp.send(null);
    oldTime = time.getTime();
    return xmlHttp.responseText;
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

document.getElementById("slider1").oninput = function () {
  var a = document.getElementById("slider1").value * -1;
  httpGet("api?a1=" + a, false);
};

document.getElementById("slider2").oninput = function () {
  var a = document.getElementById("slider2").value;
  httpGet("api?maxSpeed=" + a, false);
};
