<template>
  <div id="dashcont">
    <div v-if="showList" class="col-lg-12">
      <div class="col-md-3">
      </div>
      <div class="col-md-6" style="color: #122b40;">
        <div class="card" style="background: #fff; border-radius: 10px; padding: 20px;">
          <h1 style="text-align: center;"><i class="glyphicon glyphicon-plus"></i> NEW FAVORITE</h1>
          <div id="formz">
            <div class="form-group">
              <div class="card" style="padding: 10px;">
                <label>TITLE</label>
                <input class="form-control" v-model="title" type="text" placeholder="Title">
              </div>
            </div>
            <div class="form-group">
              <div class="card" style="padding: 10px;">
                <label>DESCRIPTION</label>
                <textarea class="form-control" v-model="description" placeholder="Description" minlength="10" rows="5"
                          cols="50" style="resize: none;"></textarea>
              </div>
            </div>
            <div class="form-group">
              <div class="card" style="padding: 10px;">
                <div class="row">
                  <div class="form-group col-md-6">
                    <label>CATEGORY</label>
                    <select class="form-control" @change="onChange($event)" v-model="category">
                      <option v-bind:key="0" value="">---SELECT---</option>
                      <option v-for="cat in cats" :key="cat.id" v-bind:value="cat.id">{{ cat.name.charAt(0).toUpperCase() + cat.name.substring(1) }}</option>
                    </select>
                  </div>
                  <div class="col-md-6 form-group">
                    <label>RANKING</label>
                    <input v-model="ranking" type="number" class="form-control">
                  </div>
                </div>
              </div>
            </div>
            <div>
              <center>
                <span v-on:click="submitList" class="btn btn-default btn-lg"
                      style="color: #122b40; font-weight: bolder;">{{submitBt}}<spinner
                v-if="submitSpinner"></spinner></span>
              </center>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3"></div>
    </div>
    <Lists v-if="!showList" v-bind:myCats="cats" v-bind:activeUserr="activeUser" />
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import Lists from '../components/Lists'
const API_URL = 'https://www.spibes.com'
export default {
  name: 'Dashboard',
  components: {Lists},
  props: ['activeUser', 'showList', 'hideList'],
  create () {
    console.log(this.showList)
  },
  data () {
    return {
      cats: [],
      submitBt: 'SUBMIT',
      submitSpinner: false,
      ranking: '',
      category: '',
      description: '',
      title: ''
    }
  },
  created () {
    this.fetchCats(this.activeUser)
  },
  methods: {
    onChange (event) {
      this.category = event.target.value
    },
    fetchCats (who) {
      const url = `${API_URL}/api/category/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        // console.log(response.data)
        this.cats = response.data
      })
    },
    submitList () {
      this.submitBt = ''
      this.submitSpinner = true
      if (this.title.length > 0) {
        if (this.description.length > 0) {
          if (this.category.length > 0) {
            if (this.ranking.length > 0 && parseInt(this.ranking) > 0) {
              // console.log(this.category)
              const url = `${API_URL}/api/list/`
              return axios.post(
                url,
                {
                  email: this.activeUser,
                  title: this.title,
                  des: this.description,
                  cat: this.category,
                  ranking: this.ranking
                },
                {
                  headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                  }
                }).then((response) => {
                // console.log(response.data)
                this.submitBt = 'SUBMIT'
                this.submitSpinner = false
                if (response.data.done) {
                  this.title = ''
                  this.description = ''
                  this.category = ''
                  this.ranking = ''
                  this.$notify({
                    type: 'success',
                    group: 'foo',
                    title: 'SUCCESS',
                    duration: 5000,
                    text: response.data.msg
                  })
                } else {
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
              this.submitBt = 'SUBMIT'
              this.submitSpinner = false
              this.$notify({
                type: 'error',
                group: 'foo',
                title: 'ERROR',
                duration: 5000,
                text: 'Oops! Ranking field is required and must be greater than zero.'
              })
            }
          } else {
            this.submitBt = 'SUBMIT'
            this.submitSpinner = false
            this.$notify({
              type: 'error',
              group: 'foo',
              title: 'ERROR',
              duration: 5000,
              text: 'Oops! Category field is required.'
            })
          }
        } else {
          this.submitBt = 'SUBMIT'
          this.submitSpinner = false
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: 'Oops! Description field is required.'
          })
        }
      } else {
        this.submitBt = 'SUBMIT'
        this.submitSpinner = false
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! Title field is required.'
        })
      }
    }
  }
}
</script>
<style scoped>
  .form-group {
    text-align: left;
  }
</style>
