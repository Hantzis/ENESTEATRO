<template>
  <q-layout view="lhh lpR fFf">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="leftDrawer = !leftDrawer"/>
        <q-toolbar-title>
          Los Falconi
        </q-toolbar-title>
        {{ todaysDate }}
      </q-toolbar>
      <!-- <q-tabs align="right">
        <q-route-tab to="" label="Uno"/>
        <q-route-tab to="" label="Dos"/>
        <q-route-tab to="" label="Tres"/>
      </q-tabs> -->
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      :breakpoint="400"
    >
      <q-scroll-area style="height: calc(100% - 142px); margin-top: 142px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item to="/" clickable v-ripple exact>
            <q-item-section avatar>
              <q-icon name="home"/>
            </q-item-section>

            <q-item-section>
              Inicio
            </q-item-section>

          </q-item>
          <q-item to="registros" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-file-edit"/>
            </q-item-section>

            <q-item-section>
              Registros
            </q-item-section>
          </q-item>

          <q-separator></q-separator>

          <q-item to="archivos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-semantic-web"/>
            </q-item-section>
            <q-item-section>
              Archivos
            </q-item-section>
          </q-item>

          <q-item to="fondos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="inbox"/>
            </q-item-section>

            <q-item-section>
              Fondos
            </q-item-section>
          </q-item>

          <q-item to="lugares" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="place"/>
            </q-item-section>

            <q-item-section>
              Lugares
            </q-item-section>
          </q-item>

          <q-item to="ramos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-source-repository"/>
            </q-item-section>

            <q-item-section>
              Ramos
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar('mathereall@gmail.com', 150)">
          </q-avatar>
          <div class="text-weight-bold">César Benjamín García Martínez</div>
          <div>mathereall@gmail.com</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <keep-alive>
        <router-view/>
      </keep-alive>
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar style="min-height: 30px;">
        <q-toolbar-title style="font-size: 12px;">
          2020 &copy; UDIR - ENES Morelia
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
  import {date} from 'quasar'
  import md5 from 'crypto-md5';

  export default {
    data() {
      return {
        leftDrawer: false
      }
    },
    computed: {
      todaysDate() {
        let timeStamp = Date.now()
        return date.formatDate(timeStamp, 'YYYY-MM-DD')
      }
    },
    methods: {
      get_gravatar(email, argsize) {
        const size = argsize
        return 'https://www.gravatar.com/avatar/' + md5(email.trim().toLowerCase(), 'hex') + '.jpg?s=' + size;
      }
    }
  }
</script>
