<template>
  <q-page padding>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" align="right">
        <q-btn color="primary" style="margin-right: 12px;">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn color="green" @click="dialogo_nuevarchivo = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Nuevo Archivo</div>
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col">

        <q-table
          title="Archivos"
          :data.sync="datos_archivos"
          :columns="columns"
          row-key="id"
          :grid="$q.screen.xs"
          :loading="loading"
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
              <q-btn dense round flat color="grey" @click="editRow(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="grey" @click="deleteRow(props)" icon="delete"></q-btn>
            </q-td>
          </template>

        </q-table>
      </div>
    </div>
  </q-page>
</template>

<script>
import firebaseDB from "boot/firebase"

export default {
  name: 'Archivos',
  data() {
    return {
      filter: '',
      loading: false,
      columns: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {name: 'nombre', align: 'left', label: 'Nombre de Archivo', field: 'nombre', sortable: true},
        { name: 'actions', label: 'Actions', field: '', align:'center' },
      ],
      datos_archivos: [],
      noti: () => {},
    }
  },
  mounted() {
    // get initial data from server (1st page)
    /*this.onRequest({
      pagination: this.pagination,
      filter: undefined
    })*/
    this.loading = true
    this.getArchivos().then((response) => {
      console.log("response:", response)
      this.loading = false
    })


  },
  methods: {
    async getArchivos() {
      try {
        const resDB = await firebaseDB.collection('Archivo').get()
        resDB.forEach(res => {
          console.log("res: ", res)
          console.log("res: ", res.id)
          console.log("res: ", res.data().nombre)
          console.log("res: ", res.data())
          const archivo = {id: res.id, nombre: res.data().nombre}
          this.datos_archivos.push(archivo)
        })
        return resDB
      } catch (error) {
        console.log(error)
      }
    },
    editRow(props) {
      this.noti()
      // do something
      this.noti = this.$q.notify({
        type: 'info',
        textColor: 'grey-10',
        multiLine: true,
        message: `I'll edit row data => ${JSON.stringify(props.row).split(',').join(', ')}`,
        timeout: 2000
      })
    },
    deleteRow(props){
      this.noti()
      // do something
      this.noti = this.$q.notify({
        type: 'negative',
        multiline: true,
        message: `I'll delete row data => ${JSON.stringify(props.row).split(',').join(', ')}`,
        timeout: 2000
      })
    }

  }
}
</script>
