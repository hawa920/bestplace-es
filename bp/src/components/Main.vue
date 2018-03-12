<template lang="pug">
    v-app
        v-toolbar(dark :color='!mode ? "pink lighten-1" : "blue lighten-1"' fixed app)
            v-toolbar-side-icon(@click.stop='drawer = !drawer'): v-icon mdi-instagram

            v-toolbar-title {{mode ? "BestPlace Taiwan" : "BestFood Taiwan" }}
            v-spacer
            v-btn(icon)
                v-icon mdi-cake
            v-btn(style='margin-right: 25px!important' icon)
                v-icon mdi-bell
        v-content
             v-container(fill-height align-center)
                v-layout.text-xs-center(align-center wrap)
                    v-flex(xs12 md6 offset-md3)
                        h2.amaze-title(v-if='mode' @mouseenter='flag=false' @mouseleave='flag=true') Find Some Amazing Place To Go&nbsp;
                            span(v-show='flag') 🙌
                            span(v-show='!flag') 👐
                        h2.amaze-title(v-else @mouseenter='flag=false' @mouseleave='flag=true') Find Some Amazing Food To Eat&nbsp;
                            span(v-show='flag') 🍰
                            span(v-show='!flag') 🍔
                        v-text-field.mt-5.mx-5(autofocus label='Hit The Road' v-model='keyword' @keyup.enter='search')
                        v-btn(dark large color='orange darken-1' @click='search' :loading='loading')
                            v-icon mdi-magnify
                            | &nbsp;搜尋&nbsp;&nbsp;&nbsp;
                        v-btn(dark large color='red lighten-1' @click='changeMode')
                            v-icon mdi-cat
                            | &nbsp;{{ mode ? "肚子餓？" : "出去玩？"}}
                    v-flex.mt-3(md6 offset-md3 lg4 offset-lg4 d-flex v-for='item in content' :key='item._id')
                        v-card.elevation-3
                            v-container.pa-0
                                v-layout(wrap)
                                    v-flex(xs12)
                                        v-card-media.white--text(height=400 :src='item._source.imgURL')
                                    v-flex(xs12)
                                        v-card-title {{ item._source.description }}
                                        v-card-actions
                                            v-spacer
                                            v-btn(flat color='orange' :href='item._source.postURL' target='_blank' rel='noopener') Detail
                                            v-spacer
                                            //v-btn(flat color='red')
        v-fab-transition
            v-btn(fixed aria-label='fab' bottom right dark fab color='red' @click='toTop' style='margin: 12px 10px;')
                v-icon mdi-chevron-up

</template>

<script>
import axios from 'axios'

export default {
    name: 'HelloWorld',
    data: () => ({
        flag: true,
        loading: false,
        keyword: '',
        content: [],
        mode: true,
        header: 'Best Place in Taiwan'

    }),
    methods: {
        toTop () {
            window.scroll({ top: 0, behavior: 'smooth' })
        },
        async search () {
            this.loading = true
            console.log(this.keyword.split(' '))
            // let result = await axios.get(`http://localhost:9200/bpintaiwan/posts/_search?q=${this.keyword}`)
            let data = { query: { match: {description: `${this.keyword}`} } }
            let result = null
            if (this.mode) {
                result = await axios.post('http://localhost:9200/bpintaiwan/posts/_search?size=20', data)
            } else {
                result = await axios.post('http://localhost:9200/bfintaiwan/posts/_search?size=20', data)
            }

            this.content = result.data.hits.hits
            setTimeout(() => { this.loading = false }, 1000)
            this.toTop()
            console.log(result.data)
        },

        changeMode () {
            this.mode = !this.mode
            this.content = []
            this.keyword = ''
        }
    }
}
</script>

<style lang="stylus">
    @import '../assets/style'
</style>
