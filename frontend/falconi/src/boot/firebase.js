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
firebaseDB.enablePersistence().catch(err => {
  console.log(err)
  alert(err)
  if (err.code == 'failed-precondition') {
    // Multiple tabs open, persistence can only be enabled
    // in one tab at a a time.
    // ...
    console.log(err)
  } else if (err.code == 'unimplemented') {
    // The current browser does not support all of the
    // features required to enable persistence
    // ...
    console.log(err)
  }
})

export default firebaseDB;
