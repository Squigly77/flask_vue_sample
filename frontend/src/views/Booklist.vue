<template>
  <div class="booklist">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <h1>ブックリスト</h1>
          <table class="table table-hover table-striped">
            <thead>
              <tr class="table-info">
                <th>id</th>
                <th>タイトル</th>
                <th>著者</th>
                <th>出版社</th>
                <th>更新</th>
                <th>削除</th>
              </tr>
            </thead>
            <tbody v-if="!edit">
              <tr v-for="(item,index) in items" :key="index">
                <td>{{item.id}}</td>
                <td>{{item.title}}</td>
                <td>{{item.author}}</td>
                <td>{{item.publisher}}</td>
                <td>
                  <b-button v-if="!edit" @click="Edit(item.id)" size="sm">Edit</b-button>
                </td>
                <td>
                  <b-button @click="del(item.id,index)" variant="danger" size="sm">Del</b-button>
                </td>
              </tr>
            </tbody>
            <tbody v-if="edit">
              <tr v-for="item in items" :key="item.id">
                <td>{{item.id}}</td>
                <td v-if="itemid == item.id"><input v-model="item.title" size="10" /></td>
                <td v-else>{{item.title}}</td>
                <td v-if="itemid == item.id"><input v-model="item.author" size="10" /></td>
                <td v-else>{{item.author}}</td>
                <td v-if="itemid == item.id"><input v-model="item.publisher" size="10" /></td>
                <td v-else>{{item.publisher}}</td>
                <td v-if="itemid == item.id">
                  <b-button
                    @click="update(item.id,item.title,item.author,item.publisher)" size="sm">update
                  </b-button>
                </td>
                <td v-else></td>
                <td v-if="itemid == item.id">
                  <b-button @click="cancel" size="sm">Cancel</b-button>
                </td>
                <td v-else></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <b-container>
        <b-row v-for="text in texts" :key="text">
          <b-col sm="3">
            <label>{{ text }}:</label>
          </b-col>
          <b-col sm="6">
            <b-form-input :id="text" type="text" class="mb-2"></b-form-input>
          </b-col>
        </b-row>
        <b-button @click="add">登録</b-button>
      </b-container>
    </div>
  </div>
</template>

<script>
const axios = require("axios").create()

export default {
  name: "booklist",
  data() {
    return {
      items: [],
      edit: false,
      itemid: "",
      texts: ["title", "author", "publisher"]
    };
  },
  mounted() {
    this.getItems()
  },
  methods: {
    getItems() {
      /* eslint-disable */
      const response = axios.get("http://localhost:5000/api/bookapp")
        .then(response => {
          console.log(response.data)
          this.items = response.data
        }).catch(error => {
          console.log(error.response.data)
        })
    },
    update(id, title, author, publisher) {
      const updatedata = {
        id: id,
        title: title,
        author: author,
        publisher: publisher
      }
      axios.put("http://localhost:5000/api/bookapp", updatedata)
        .then(response => {
          this.edit = false
          console.info(response.data.message)
        }).catch(error => {
          console.log(error.response.data)
        })
    },
    Edit(id) {
      this.edit = true
      this.itemid = id
    },
    cancel() {
      this.edit = false
    },
    del(id,index) {
      const data = { id: id }
      axios.delete("http://localhost:5000/api/bookapp", { data: data })
        .then(response => {
          this.items.splice(index, 1)
          console.info(response.data.message)
        })
    },
    add() {
      var title = document.getElementById("title").value
      var author = document.getElementById("author").value
      var publisher = document.getElementById("publisher").value
      const params = { title: title, author: author, publisher: publisher }
      axios.post("http://localhost:5000/api/bookapp", params)
        .then(response => {
          const id = response.data
          const newitem = {
            id: id,
            title: title,
            author: author,
            publisher: publisher
          }
          this.items.push(newitem)
          console.log(response)
        }).catch(error => {
          console.log(error.response.data)
        })
    }
  }
}
</script>