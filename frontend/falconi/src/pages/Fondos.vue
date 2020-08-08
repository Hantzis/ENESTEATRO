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
        <q-btn color="green" @click="addFondoDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Fondo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Fondos"
          :data.sync="Object.values(datos_fondos)"
          :columns="columns"
          row-key="id"
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
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="green" text-color="white"/>
          <q-toolbar-title>Agregar nuevo fondo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del fondo" v-model="fondo_nombre"
                       :error-message="mensaje_error" :error="fondonuevo_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Agregar" color="primary" v-close-popup
                 :disable="fondonuevo_invalido || !this.fondo_nombre"
                 @click="addFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_editarfondo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="edit" color="primary" text-color="white"/>
          <q-toolbar-title>Editar fondo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-input name="nombre" label="Nombre del fondo" v-model="fondo_nombre"
                       :error-message="mensaje_error" :error="fondomodificado_invalido"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="secondary" v-close-popup @click="cancelar_guardado()"/>
          <q-btn flat label="Guardar" color="primary" v-close-popup
                 :disable="fondomodificado_invalido || !this.fondo_nombre"
                 @click="updateFondo()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dialogo_eliminarfondo" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="red" text-color="white"/>
          <q-toolbar-title>Eliminar fondo</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <p>¿Está seguro de eliminar este fondo?</p>
          </div>
          <div class="row">
            <div class="col">
              <q-input readonly name="nombre" label="Nombre del fondo" v-model="fondo_nombre"/>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
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
      fondo_nombre: undefined,
      fondo_nombre_id: undefined,
      columns: [
        {name: 'nombre', align: 'left', label: 'Nombre de Fondo', field: 'nombre', sortable: true},
        {name: 'actions', label: '', field: 'actions', align: 'right'},
      ],
      datos_fondos: [],
      firebaseRef: firebaseDB.collection('Fondo'),
    }
  },
  mounted() {
    this.getFondos()
  },
  created() {
    this.firebaseRef.onSnapshot({includeMetadataChanges: false}, snapshot => {
      this.tabla_loading = true
      if (!((snapshot.docs.length === snapshot.docChanges().length) && snapshot.docChanges().length > 1)) {
        snapshot.docChanges().forEach(change => {
          this.getFondos()
          if (change.type === "added") {
            this.$q.notify({
              type: 'positive',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se agregó el nuevo fondo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "removed") {
            this.$q.notify({
              type: 'negative',
              multiLine: true,
              message: `Se eliminó el fondo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          } else if (change.type === "modified") {
            this.$q.notify({
              type: 'info',
              textColor: 'grey-10',
              multiLine: true,
              message: `Se modifico el fondo "${change.doc.data().nombre}"`,
              timeout: 2000
            })
          }
        })
      }
      this.fondo_nombre = undefined;
      this.fondo_id = undefined;
      this.tabla_loading = false
    }, error => {
      console.log("error", error)
    }, () => {
      console.log("Complete")
    })
  },
  methods: {
    getFondos() {
      this.tabla_loading = true
      console.log("get fondos")
      this.firebaseRef.get().then(response => {
        this.datos_fondos = {}
        response.forEach(res => {
          this.datos_fondos[res.id] = {id: res.id, nombre: res.data().nombre}
        })
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
      })
    },
    addFondo() {
      this.tabla_loading = true
      this.firebaseRef.add({nombre: this.fondo_nombre})
      this.tabla_loading = false
    },
    updateFondo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.fondo_id).update({nombre: this.fondo_nombre})
      this.tabla_loading = false
    },
    deleteFondo() {
      this.tabla_loading = true
      this.firebaseRef.doc(this.fondo_id).delete()
      this.tabla_loading = false
    },
    cancelar_guardado() {
      this.fondo_nombre = undefined
      this.fondo_id = undefined
    },
    addFondoDialog() {
      this.dialogo_nuevofondo = true
    },
    editFondoDialog(props) {
      console.log(props)
      this.dialogo_editarfondo = true
      this.fondo_nombre = props.row.nombre
      this.fondo_id = props.row.id
    },
    deleteFondoDialog(props) {
      console.log(props)
      this.dialogo_eliminarfondo = true
      this.fondo_nombre = props.row.nombre
      this.fondo_id = props.row.id
    },
  },
  computed: {
    fondonuevo_invalido() {
      if (this.fondo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_fondos)) {
          if (item.nombre === this.fondo_nombre) {
            existe = true
          }
        }
        return this.fondo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    fondomodificado_invalido() {
      if (this.fondo_nombre) {
        let existe = false;
        for (let item of Object.values(this.datos_fondos)) {
          if (item.nombre === this.fondo_nombre && item.id !== this.fondo_id) {
            existe = true
          }
        }
        return this.fondo_nombre.length < 1 || existe
      } else {
        return false
      }
    },
    mensaje_error() {
      let mensaje = ""
      for (let item of Object.values(this.datos_fondos)) {
        if (item.nombre === this.fondo_nombre) {
          mensaje += "Ya existe un fondo con ese nombre. "
        }
      }
      return mensaje
    }
  }
}
</script>
