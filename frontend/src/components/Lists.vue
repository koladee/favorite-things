<template>
  <div id="listCont">
    <roller v-if="mainLoader"></roller>
    <div v-if="!mainLoader">
      <div class="col-lg-12">
        <div class="col-md-2">
        </div>
        <div class="col-md-8" style="color: #122b40;">
          <div class="card" style="background: #fff; border-radius: 10px; padding: 20px;">
            <div class="row">
              <div class="col-md-6">
                <div class="row">
                  <div class="form-group col-md-9" style="padding-right: 0px;">
                    <input v-model="newCat" type="text" class="form-control" placeholder="New Category"
                           style="border-top-right-radius: 0px; border-bottom-right-radius: 0px;">
                  </div>
                  <div class="form-group col-md-3" style="padding-left: 0px;">
                    <span id="new-cat-bt" v-on:click="addNewCat" class="btn btn-primary btn-block"
                          style="border-top-left-radius: 0px; border-bottom-left-radius: 0px; font-weight: bolder;">
                      <i v-bind:class="newCatBtClass"></i> {{newCatBt}}<spinner v-if="newCatSpinner"></spinner></span>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <select class="form-control" @change="onChange($event)" v-model="category">
                    <option value="">Sort By All Categories</option>
                    <option v-for="cat in myCats" :key="cat.id" v-bind:value="cat.id">Sort By {{
                      cat.name.charAt(0).toUpperCase() + cat.name.substring(1) }} Category
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-2">
                <br><br>
              </div>
            </div>

            <br>
            <roller v-if="listLoader"></roller>
            <div v-if="!listLoader" id="list-cont" style="min-height: 300px;">
              <div v-for="(list, k) in lists" :key="k" class="row card" style="width: 100%; min-height: 250px; padding: 20px; margin-left: 0px;">
                <div class="col-md-8">
                  <div class="form-group">
                    <label>TITLE</label>
                    <input v-bind:id="list.rid+list.id+'title'"  class="form-control" type="text" readonly v-bind:value="list.title">
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label>DATE CREATED</label>
                    <input class="form-control" type="date" readonly v-model="list.created_date.split('T')[0]">
                  </div>
                </div>
                <div class="col-md-8">
                  <div class="form-group">
                    <label>DESCRIPTION</label>
                    <textarea v-bind:id="list.rid+list.id+'description'" class="form-control" style="resize: none" rows="10" readonly v-bind:value="list.description" ></textarea>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label>CATEGORY</label>
                    <select v-bind:id="list.rid+list.id+'cat'" class="form-control" disabled  v-bind:value="list.cat">
                      <option v-for="cat in myCats" :key="cat.id" v-bind:value="cat.id">{{
                        cat.name.charAt(0).toUpperCase() + cat.name.substring(1) }}
                      </option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>RANKING</label>
                    <input v-bind:id="list.rid+list.id+'ranking'" type="number" class="form-control" readonly v-model="list.ranking">
                  </div>
                  <div class="form-group">
                    <div class="alert alert-info">
                      Last Modified:
                      <span>{{ list.modified_date.split('T')[0]}}</span>
                    </div>
                  </div>
                  <div class="form-group">
                    <span v-bind:id="list.rid+list.id+'editBt'" v-on:click="editList(list.rid, list.id)" class="btn btn-default" style="font-weight: bolder;"><i class="glyphicon glyphicon-pencil"></i> EDIT</span>
                    <span v-bind:id="list.rid+list.id+'saveEditBt'" v-on:click="saveList(list.rid, list.id)" class="btn btn-default hidden" style="font-weight: bolder;"><i class="glyphicon glyphicon-save"></i> SAVE</span>
                    <span v-bind:id="list.rid+list.id+'saveEditBtSpinner'" class="btn btn-default hidden"><spinner></spinner></span>
                    <span v-bind:id="list.rid+list.id+'logBt'" v-on:click="showLog(list.rid, list.id)" class="btn btn-primary" style="font-weight: bolder;"><i class="glyphicon glyphicon-time"></i> LOGS</span>
                  </div>
                </div>
                <div class="col-md-12">
                  <div v-bind:id="list.rid+list.id+'logs'" class="hidden">{{list.log}}</div>
                  <div v-bind:id="list.rid+list.id+'logsCont'" class="hidden" style="background: #0f0f0f; color: #eee; padding-bottom: 0px; margin-bottom: 0px; height: 200px;
                   overflow-y: auto">
                    <span class="btn btn-default" style="float: right;" v-on:click="hideLog(list.rid, list.id)">&times;</span>
                    <span v-if="list.log !== ''" v-for="(log, x) in list.log.split('{:||:}')" :key="x"><span v-if="log !== ''" v-html="'>>> '+log.split('(+||+)')[0]"></span><span v-if="log !== ''" v-html="'['+log.split('(+||+)')[1]+']<br>'" style="margin-left: 20px;"></span> </span>
                    <span v-if="list.log === ''">>>> Log record is empty </span>
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
const API_URL = 'https://www.spibes.com'
export default {
  name: 'Lists',
  props: ['myCats', 'activeUserr'],
  data () {
    return {
      mainLoader: true,
      listLoader: true,
      category: '',
      newCat: '',
      newCatBt: 'ADD',
      newCatSpinner: false,
      newCatBtClass: 'glyphicon glyphicon-plus',
      lists: [],
      logs: []
    }
  },
  created () {
    this.mainLoader = false
    this.fetchList('')
  },
  methods: {
    fetchList (a) {
      this.listLoader = true
      if (a.length === 0) {
        const url = `${API_URL}/api/list/?who=${this.activeUserr}`
        return axios.get(
          url,
          {
            headers: {}
          }).then((response) => {
          // console.log(response.data)
          this.listLoader = false
          this.lists = response.data
        })
      } else {
        const url = `${API_URL}/api/list/?who=${this.activeUserr}&cat=${a}`
        return axios.get(
          url,
          {
            headers: {}
          }).then((response) => {
          // console.log(response.data)
          this.listLoader = false
          this.lists = response.data
        })
      }
    },
    onChange (event) {
      this.category = event.target.value
      this.sortList()
    },
    sortList () {
      this.fetchList(this.category)
    },
    addNewCat () {
      this.newCatBt = ''
      this.newCatBtClass = ''
      this.newCatSpinner = true
      if (this.newCat.length > 0) {
        const url = `${API_URL}/api/category/`
        return axios.post(
          url,
          {
            email: this.activeUserr,
            name: this.newCat
          },
          {
            headers: {
              'X-CSRFToken': Cookies.get('csrftoken')
            }
          }).then((response) => {
          if (response.data.done) {
            this.newCatBt = 'ADD'
            this.newCatBtClass = 'glyphicon glyphicon-plus'
            this.newCatSpinner = false
            this.newCat = ''
            this.$notify({
              type: 'success',
              group: 'foo',
              title: 'SUCCESS',
              duration: 5000,
              text: response.data.msg
            })
          } else {
            this.newCatBt = 'ADD'
            this.newCatBtClass = 'glyphicon glyphicon-plus'
            this.newCatSpinner = false
            this.$notify({
              type: 'error',
              group: 'foo',
              title: 'ERROR',
              duration: 5000,
              text: response.data.msg
            })
          }
        })
      } else {
        this.newCatBt = 'ADD'
        this.newCatBtClass = 'glyphicon glyphicon-plus'
        this.newCatSpinner = false
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! A new category name to be added must be specified.'
        })
      }
    },
    editList (a, b) {
      document.getElementById(a + b + 'title').removeAttribute('readonly')
      document.getElementById(a + b + 'description').removeAttribute('readonly')
      document.getElementById(a + b + 'cat').removeAttribute('disabled')
      document.getElementById(a + b + 'ranking').removeAttribute('readonly')
      document.getElementById(a + b + 'editBt').className = 'btn btn-default hidden'
      document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
    },
    saveList (a, b) {
      const title = document.getElementById(a + b + 'title')
      const des = document.getElementById(a + b + 'description')
      const cat = document.getElementById(a + b + 'cat')
      const rank = document.getElementById(a + b + 'ranking')
      if (title.value.length > 0) {
        if (des.value.length > 0) {
          if (cat.value.length > 0) {
            if (rank.value.length > 0 && parseInt(rank.value) > 0) {
              document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default'
              document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default hidden'
              const url = `${API_URL}/api/list/`
              return axios.put(
                url,
                {
                  id: b,
                  email: this.activeUserr,
                  title: title.value,
                  des: des.value,
                  cat: cat.value,
                  ranking: rank.value
                },
                {
                  headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                  }
                }).then((response) => {
                // console.log(response.data)
                if (response.data.done) {
                  title.setAttribute('readonly', 'readonly')
                  des.setAttribute('readonly', 'readonly')
                  cat.setAttribute('disabled', 'disabled')
                  rank.setAttribute('readonly', 'readonly')
                  document.getElementById(a + b + 'editBt').className = 'btn btn-default'
                  document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default hidden'
                  document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
                  this.$notify({
                    type: 'success',
                    group: 'foo',
                    title: 'SUCCESS',
                    duration: 5000,
                    text: 'Favorite list successfully edited.'
                  })
                  this.fetchList(this.category)
                } else {
                  document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
                  document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
                  this.$notify({
                    type: 'error',
                    group: 'foo',
                    title: 'ERROR',
                    duration: 5000,
                    text: response.data.msg
                  })
                }
              })
            } else {
              document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
              document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
              this.$notify({
                type: 'error',
                group: 'foo',
                title: 'ERROR',
                duration: 5000,
                text: 'Oops! Ranking field is required and must be greater than zero.'
              })
            }
          } else {
            document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
            document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
            this.$notify({
              type: 'error',
              group: 'foo',
              title: 'ERROR',
              duration: 5000,
              text: 'Oops! Category field is required.'
            })
          }
        } else {
          document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
          document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: 'Oops! Description field is required.'
          })
        }
      } else {
        document.getElementById(a + b + 'saveEditBtSpinner').className = 'btn btn-default hidden'
        document.getElementById(a + b + 'saveEditBt').className = 'btn btn-default'
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! Title field is required.'
        })
      }
    },
    showLog (a, b) {
      const logs = document.getElementById(a + b + 'logs').innerHTML
      this.logs = logs.split('{:||:}')
      document.getElementById(a + b + 'logsCont').className = ''
    },
    hideLog (a, b) {
      this.logs = []
      document.getElementById(a + b + 'logsCont').className = 'hide'
    }
  }
}
</script>

<style scoped>
  .form-group {
    text-align: left;
  }
</style>
