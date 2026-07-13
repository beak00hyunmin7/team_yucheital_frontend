// //1. number
// var number = 1;
// console.log(typeof number, number);

// //2. string
// var string = 'hello';
// console.log(typeof string, string);
// var string2 = 'world';
// console.log(`backtick: ${string} ${string2}`);

// //3. Boolean
// var boolean = true;
// console.log(typeof boolean, boolean);

// //4. undefined
// var undefined;
// console.log(typeof undefined, undefined);

// //5. null
// var b = null;
// console.log(typeof b, b);
// if (b === null) console.log(b, "is null");

// //6. Symbol -> 유일키
// var sym = Symbol("symbolic");
// console.log(typeof sym, sym);

// var sym2 = Symbol("symbolic");
// console.log(sym === sym2);

// console.log("=========객체타입=========");

// //object
// var obj = {};
// console.log(typeof obj, obj);

// var person = {
//     name : "hyunmin",
//     age : 20,
//     say : function() {
//         console.log("hello");
//     }
// };

// console.log(person.name);
// console.log(person.age);
// console.log(person.say());


// var num = 1;
// console.log(num)
// let string = "asdf";
// console.log(string)
// const a = null;
// console.log(a)
// var b;
// console.log(b)
// var boolean = true;
// console.log(boolean)
// var sym = Symbol();
// console.log(sym)
// var obj = {};
// console.log(obj)


// //1. 블록문
// {
//     var number = 1;
//     console.log(1);
// }

// //2. 조건문
// var gender = "man";
// if (gender === "man") console.log("you are man");
// else console.log("you are woman");

// switch (gender){
//     case "man":
//         console.log("you are man!");
//         break;
//     case "woman":
//         console.log("you are woman!");
//         break;
//     default:
//         console.log("asdf");
//         break;
// }

// //3. 반복문
// for (var i = 0; i < 5; i++) {
//     console.log(`${i}th loop`);
// }
// console.log(i);

// i = 0;
// while (i < 5) {
//     console.log(`${i}th loop`);
//     i++;
// }
// console.log(i);

// var a = 0;
// if (typeof a === "number"){
//     console.log("a is number");
// }
// else if (typeof a === "string"){
//     console.log("a is string");
// }
// else console.log("a is something else");

// for (var i = 0; i <= 10; i ++){
//     if (i % 2 === 1) console.log(`${i} is odd`);
// }

// var input;
// input = prompt();
// console.log(input);
// if (input === "1") console.log("input is 1");


import * as THREE from 'three'; // three.js 라이브러리 전체를 불러오기

const container = document.getElementById( 'three-container' ); // 큐브를 그릴 영역(오른쪽 일부)

const scene = new THREE.Scene(); // 3D 장면 생성

// 카메라 생성: 화각 75도, 화면 비율은 전체 창이 아닌 컨테이너 크기 기준, near/far 클리핑 범위(0.1~1000)
const camera = new THREE.PerspectiveCamera( 75, container.clientWidth / container.clientHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer(); // WebGL로 화면을 그려주는 렌더러 생성
renderer.setSize( container.clientWidth, container.clientHeight ); // 렌더러 크기를 컨테이너 크기에 맞춤
renderer.setAnimationLoop( animate ); // 매 프레임마다 animate 함수를 반복 호출
container.appendChild( renderer.domElement ); // 렌더러가 그리는 canvas를 컨테이너 안에 추가

window.addEventListener( 'resize', () => { // 창 크기가 바뀌면 컨테이너 크기에 맞춰 다시 계산
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize( container.clientWidth, container.clientHeight );
} );

const geometry = new THREE.BoxGeometry( 1, 1, 1 ); // 기본 1x1x1 모양 (실제 크기는 아래 scale로 조절)
const material = new THREE.MeshBasicMaterial( { color: 0xffffff } ); // 빨간색 기본 재질(조명 영향 안 받음)
const cube = new THREE.Mesh( geometry, material ); // 모양(geometry) + 재질(material)을 합쳐 실제 오브젝트 생성
cube.scale.set( 1.5, 1.5, 1.5 ); // 처음 가로/세로/높이 값 (입력칸 기본값과 동일)
scene.add( cube ); // 생성한 큐브를 장면에 추가

camera.position.z = 5; // 카메라를 z축으로 5만큼 뒤로 이동시켜 큐브가 보이게 함

// 왼쪽 폼 제출 시 입력한 가로/세로/높이 값으로 큐브 크기를 실시간으로 변경
const sizeForm = document.getElementById( 'sizeForm' );
sizeForm.addEventListener( 'submit', ( e ) => {
  e.preventDefault(); // 폼 제출 시 페이지가 새로고침되는 기본 동작 막기

  const width = Number( document.getElementById( 'boxWidth' ).value );
  const height = Number( document.getElementById( 'boxHeight' ).value );
  const depth = Number( document.getElementById( 'boxDepth' ).value );

  cube.scale.set( width, height, depth ); // geometry를 새로 만들지 않고 크기만 조절
} );

function animate( time ) { // time: setAnimationLoop가 넘겨주는 현재 시각(ms)

  cube.rotation.x = time / 1000; // 시간에 비례해 큐브를 x축 기준으로 회전
  cube.rotation.y = time / 500; // 시간에 비례해 큐브를 y축 기준으로 회전(x축보다 2배 빠르게)

  renderer.render( scene, camera ); // 현재 장면을 카메라 시점으로 렌더링

}