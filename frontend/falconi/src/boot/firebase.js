import firebase from "firebase";

const firebaseConfig = {
  apiKey: "AIzaSyB7-T_F5cujDJXAmXFJG9nGcWIYbyKhWzQ",
  authDomain: "archivo-los-falconi-33469.firebaseapp.com",
  databaseURL: "https://archivo-los-falconi-33469.firebaseio.com",
  projectId: "archivo-los-falconi-33469",
  storageBucket: "archivo-los-falconi-33469.appspot.com",
  messagingSenderId: "509908612887",
  appId: "1:509908612887:web:3a8f081fed8b19e17a6952",
};

/* const app = firebase.initializeApp(firebaseConfig)
const firebaseDB = firebase.firestore(); */

const firebaseDB = firebase.initializeApp(firebaseConfig).firestore()

export default firebaseDB;
