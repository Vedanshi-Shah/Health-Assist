import * as firebase from "firebase";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAeI470Zy1uVLG92ivOSHAQKGWvUb0rywg",
    authDomain: "healthassist-aed4f.firebaseapp.com",
    databaseURL: "https://healthassist-aed4f-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "healthassist-aed4f",
    storageBucket: "healthassist-aed4f.appspot.com",
    messagingSenderId: "266260061032",
    appId: "1:266260061032:web:9f9132dd4dda99dff914dd"
  };
  

// Initialize Firebase
let app;
if (firebase.apps.length === 0) {
  app = firebase.initializeApp(firebaseConfig);
} else {
  app = firebase.app()
}

const auth = firebase.auth()

export { auth };