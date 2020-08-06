<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Fondos" icon="inbox"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" style="margin-right: 12px;" @click="getFondos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevofondo = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Fondo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Fondos"
          :data.sync="datos_fondos"
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
              <q-btn dense round flat color="primary" @click="editFondoDialog(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="red" @click="deleteFondoDialog(props)" icon="delete"></q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dialogo_nuevofondo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Agregar nuevo fondo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del fondo" v-model="nuevo_fondo_nombre"
                       :error-message="mensaje_error" :error="fondonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar nuevo" color="primary" v-close-popup
                 :disable="fondonuevo_invalido || !this.nuevo_fondo_nombre"
                 @click="addFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarfondo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>Editar fondo</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del fondo" v-model="editar_fondo_nombre"
                       :error-message="mensaje_error" :error="fondonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar edición" color="primary" v-close-popup
                 :disable="fondomodificado_invalido || !this.editar_fondo_nombre"
                 @click="saveFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarfondo" persistent>
      <q-card>
        <q-card-section class="">
          <div class="row">
            <p>¿Está seguro de eliminar este fondo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del fondo" v-model="eliminar_fondo_nombre"
                       :error-message="mensaje_error" :error="fondonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Eliminar" color="red" v-close-popup
                 @click="deleteFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"

export default {
  name: 'Fondos',
  data() {
    return {
      filter: '',
      tabla_loading: false,
      dialogo_nuevofondo: false,
      dialogo_editarfondo: false,
      dialogo_eliminarfondo: false,
      nuevo_fondo_nombre: undefined,
      editar_fondo_nombre: undefined,
      editar_fondo_id: undefined,
      eliminar_fondo_nombre: undefined,
      eliminar_fondo_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Fondo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_fondos: [],
      noti: () => {
      },
    }
  },
  mounted() {
    this.getFondos()
  },
  methods: {
    async getFondos() {
      try {
        const resDB = await firebaseDB.collection('Fondo').get()
        this.datos_fondos = []
        resDB.forEach(res => {
          const fondo = {id: res.id, nombre: res.data().nombre}
          this.datos_fondos.push(fondo)
        })
        this.tabla_loading = false
        return resDB
      } catch (error) {
        console.log(error)
        this.tabla_loading = false
      }
    },
    async addFondo() {
      try {
        const resDB = await firebaseDB.collection('Fondo').add({nombre: this.nuevo_fondo_nombre})
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se agregó el nuevo fondo "${this.nuevo_fondo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.nuevo_fondo_nombre = undefined
        await this.getFondos()
      }
    },
    async saveFondo() {
      try {
        await firebaseDB.collection('Fondo').doc(
          this.editar_fondo_id).update({nombre: this.editar_fondo_nombre})
        this.$q.notify({
          type: 'info',
          textColor: 'grey-10',
          multiLine: true,
          message: `Se modifico el fondo "${this.editar_fondo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.editar_fondo_nombre = undefined
        this.editar_fondo_id = undefined
        await this.getFondos()
      }
    },
    async deleteFondo() {
      try {
        await firebaseDB.collection('Fondo').doc(this.eliminar_fondo_id).delete()
        this.$q.notify({
          type: 'negative',
          multiLine: true,
          message: `Se eliminó el fondo "${this.eliminar_fondo_nombre}"`,
          timeout: 2000
        })
      } catch (error) {
        console.log(error)
      } finally {
        this.eliminar_fondo_nombre = undefined
        this.eliminar_fondo_id = undefined
        await this.getFondos()
      }
    },
    cancelar_guardado() {
      this.nuevo_fondo_nombre = undefined
      this.editar_fondo_nombre = undefined
    },
    editFondoDialog(props) {
      this.dialogo_editarfondo = true
      this.editar_fondo_nombre = props.row.nombre
      this.editar_fondo_id = props.row.id
    },
    deleteFondoDialog(props) {
      this.dialogo_eliminarfondo = true
      this.eliminar_fondo_nombre = props.row.nombre
      this.eliminar_fondo_id = props.row.id
    },
  },
  computed: {
    fondonuevo_invalido() {
      if (this.nuevo_fondo_nombre) {
        let existe = false;
        for (let item of this.datos_fondos) {
          if (item.nombre === this.nuevo_fondo_nombre) {
            existe = true
          }
        }
        return this.nuevo_fondo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    fondomodificado_invalido() {
      if (this.editar_fondo_nombre) {
        let existe = false;
        for (let item of this.datos_fondos) {
          if (item.nombre === this.editar_fondo_nombre && item.nombre !== this.editar_fondo_id) {
            existe = true
          }
        }
        return this.editar_fondo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of this.datos_fondos) {
        if (item.nombre === this.nuevo_fondo_nombre) {
          mensaje += "Ya existe un fondo con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
