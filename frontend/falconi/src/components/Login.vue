<template>
  <div class="row">
    <div class="col">
      <div class="row">
        <div class="col" style="min-width: 256px;">
          <q-form>
            <div class="row">
              <q-input class="full-width" name="email" v-model="email" label="Dirección de correo"/>
            </div>
            <div class="row">
              <q-input class="full-width" name="password" v-model="password" type="password" label="Contraseña"/>
            </div>
            <br/>

            <div class="row">
              <div class="col" align="right">
                <q-btn color="green" label="Ingresar" class="full-width"/>
              </div>
            </div>

          </q-form>
        </div>
      </div>
      <div class="row q-py-sm">
        <div class="col q-py-sm">
          <div class="row q-py-sm">
            <q-separator style="border-top: 1px dashed; background: white !important;;" color="green"/>
          </div>
          <div class="row">
            <div class="col" align="right">
              <p style="margin: 0"><a href="">Olvidé mi contraseña</a></p>
              <p style="margin: 0"><a href="" class="primary">Crear cuenta</a></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from 'firebase'
export default {
  name: "Login",
  data() {
    return {
      email: undefined,
      password: undefined,
    }
  }

}
</script>

<style scoped>

</style>
