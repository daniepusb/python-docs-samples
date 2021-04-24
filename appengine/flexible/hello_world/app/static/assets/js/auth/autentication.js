class Autentication {
    autEmailPass (email, password) {
      
  
      firebase.auth().signInWithEmailAndPassword(email, password)
      
      .then(result => {
        console.log(result)
        if (result.user.emailVerified) {
          $('#avatar').attr('src', 'imagenes/usuario_auth.png')
          Materialize.toast(`Bienvenido ${result.user.displayName}`, 5000)
        } else {
          firebase.auth().signOut()
          Materialize.toast(
            `Por favor realiza la verificación de la cuenta`,
            5000
          )
        }
      })
  
      $('.modal').modal('close')
    }
  
    crearCuentaEmailPass (email, password, nombres) {
      firebase
        .auth()
        .createUserWithEmailAndPassword(email, password)
        .then(result => {
          result.user.updateProfile({
            displayName: nombres
          })
  
          const configuracion = {
            url: 'http://localhost/firebase-blogeek-platzi'
          }
  
          result.user.sendEmailVerification(configuracion).catch(error => {
            console.error(error)
            Materialize.toast(error.message, 4000)
          })
  
          firebase.auth().signOut()
  
          Materialize.toast(
            `Bienvenido ${nombres}, debes realizar el proceso de verificación`,
            4000
          )
  
          $('.modal').modal('close')
        })
        .catch(error => {
          console.error(error)
          Materialize.toast(error.message, 4000)
        })
    }
  
    authCuentaGoogle () {
      console.log("authCuentaGoogle()")
  
      const provider = new firebase.auth.GoogleAuthProvider()
      //provider.addScope('phonenumbers')
  
      firebase.auth().signInWithPopup(provider).then(result => {
        console.log(result)
        //$('#avatar').attr('src', result.user.photoURL)
        //$('.modal').modal('close')
        M.toast({html: `Bienvenido ${result.user.displayName} !! `, displayLength:4000})
        
      })
      .catch(error =>{
        console.error(error)
        M.toast({html: `Error al autenticarse con google: ${error} `, displayLength:4000})
      })
    }
  
    authCuentaFacebook () {
      const provider = new firebase.auth.FacebookAuthProvider();
  
      firebase.auth().signInWithPopup(provider)
      
      .then(result => {
        // $('#avatar').attr('src', result.user.photoURL)
        // $('.modal').modal('close')
        M.toast({html: `Bienvenido ${result.user.displayName} !! `, displayLength:4000})
      })
      .catch(error =>{
        console.error(error)
        M.toast({html: `Error al autenticarse con Facebook: ${error} `, displayLength:4000})
      })
    }
  
    authTwitter () {
      var provider = new firebase.auth.TwitterAuthProvider();
      firebase.auth().signInWithPopup(provider).then(result => {
        console.error(result);
        var token = result.credential.accessToken;
        var secret = result.credential.secret;
        // $('#avatar').attr('src', result.user.photoURL);
        $('.modal').modal('close');
        M.toast({html: `Bienvenido ${result.user.displayName} !! `, displayLength:4000})
      })
      .catch(error =>{
        console.error(error)
        M.toast({html: `Error al autenticarse con Twitter: ${error} `, displayLength:4000})
      })
    }
  
  
    
  }