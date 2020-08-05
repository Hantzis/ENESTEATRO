<template>
  <q-page class="flex flex-center">
    <div class="row">
      <div class="col q-px-md">
        <img alt="UDIR" src="~assets/logo_udir.png" width="256">
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Login />
      </div>
    </div>

  </q-page>
</template>

<script>
import Login from "components/Login";

export default {
  name: 'PageIndex',
  components: {Login}
}
</script>
