<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Lugares" icon="place"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" style="margin-right: 12px;" @click="getLugares()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevolugar = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Lugar</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Lugares"
          :data.sync="datos_lugares"
          :columns="columns"
          row-key="id"
          :grid1="$q.screen.xs"
          :loading="tabla_loading"
          :filter="filter"
        >
          <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="editLugarDialog(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="red" @click="deleteLugarDialog(props)" icon="delete"></q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevolugar" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Agregar nuevo lugar</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del lugar" v-model="nuevo_lugar_nombre"
                       :error-message="mensaje_error" :error="lugarnuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 :disable="lugarnuevo_invalido || !this.nuevo_lugar_nombre"
                 @click="addLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarlugar" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Editar lugar</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del lugar" v-model="editar_lugar_nombre"
                       :error-message="mensaje_error" :error="lugarnuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar edición" color="primary" v-close-popup
                 :disable="lugarmodificado_invalido || !this.editar_lugar_nombre"
                 @click="saveLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarlugar" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>¿Está seguro de eliminar este lugar?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del lugar" v-model="eliminar_lugar_nombre"
                       :error-message="mensaje_error" :error="lugarnuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteLugar()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"

export default {
  name: 'Lugares',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevolugar: false,
      dialogo_editarlugar: false,
      dialogo_eliminarlugar: false,
      nuevo_lugar_nombre: undefined,
      editar_lugar_nombre: undefined,
      editar_lugar_id: undefined,
      eliminar_lugar_nombre: undefined,
      eliminar_lugar_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Lugar', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_lugares: [],
      noti: () => {
      },
    }
  },
  mounted() {
    this.getLugares()
  },
  methods: {
    async getLugares() {
      try {
        const resDB = await firebaseDB.collection('Lugar').get()
        this.datos_lugares = []
        resDB.forEach(res => {
          const lugar = {id: res.id, nombre: res.data().nombre}
          this.datos_lugares.push(lugar)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        console.log(error)
        this.tabla_loading = false
      }
    },
    async addLugar() {
      try {
        const resDB = await firebaseDB.collection('Lugar').add({nombre: this.nuevo_lugar_nombre})
        console.log(resDB.id)
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se agregó el nuevo lugar "${this.nuevo_lugar_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.nuevo_lugar_nombre = undefined
        await this.getLugares()
      }
    },
    async saveLugar() {
      try {
        await firebaseDB.collection('Lugar').doc(
          this.editar_lugar_id).update({nombre: this.editar_lugar_nombre})
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se modifico el lugar "${this.editar_lugar_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.editar_lugar_nombre = undefined
        this.editar_lugar_id = undefined
        await this.getLugares()
      }
    },
    async deleteLugar() {
      try {
        await firebaseDB.collection('Lugar').doc(this.eliminar_lugar_id).delete()
        this.$q.notify({
          type: 'negative',
          multiLine: true,
          message: `Se eliminó el lugar "${this.eliminar_lugar_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.eliminar_lugar_nombre = undefined
        this.eliminar_lugar_id = undefined
        await this.getLugares()
      }
    },
    cancelar_guardado() {
      this.nuevo_lugar_nombre = undefined
      this.editar_lugar_nombre = undefined
    },
    editLugarDialog(props) {
      this.dialogo_editarlugar = true
      this.editar_lugar_nombre = props.row.nombre
      this.editar_lugar_id = props.row.id
    },
    deleteLugarDialog(props) {
      this.dialogo_eliminarlugar = true
      this.eliminar_lugar_nombre = props.row.nombre
      this.eliminar_lugar_id = props.row.id
    },
  },
  computed: {
    lugarnuevo_invalido() {
      if (this.nuevo_lugar_nombre) {
        let existe = false;
        for (let item of this.datos_lugares) {
          if (item.nombre === this.nuevo_lugar_nombre) {
            existe = true
            console.log("existe")
          }
        }
        return this.nuevo_lugar_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    lugarmodificado_invalido() {
      if (this.editar_lugar_nombre) {
        let existe = false;
        for (let item of this.datos_lugares) {
          if (item.nombre === this.editar_lugar_nombre && item.nombre !== this.editar_lugar_id) {
            existe = true
            console.log("existe")
          }
        }
        return this.editar_lugar_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of this.datos_lugares) {
        if (item.nombre === this.nuevo_lugar_nombre) {
          mensaje += "Ya existe un lugar con ese nombre. "
          console.log("existe")
        }
      }
      return mensaje
    }
  }
}
</script>
