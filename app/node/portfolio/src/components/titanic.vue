<script setup lang='ts'>
import axios from 'axios';
import {reactive} from 'vue';


type typeOfFeatures = {
	Sex: '男性'|'女性'|'性別を教えてください'
	Pclass: string
	Age: Number|'年齢は？'
	Parch: Number|'親・子の同伴者数は？'
	SibSp: Number|'兄弟姉妹の同伴者数は？'
}

const features = reactive<typeOfFeatures>({
  Sex: '性別を教えてください',
  Pclass: '階級は？',
  Age: '年齢は？',
  Parch: '親・子の同伴者数は？',
  SibSp: '兄弟姉妹の同伴者数は？'
})

const displayOutput = ():void => {
alert(`
     性別: ${features.Sex}
     階級: ${features.Pclass}
     年齢: ${features.Age}
     親・子同伴者数: ${features.Parch}
     兄弟姉妹同伴者数: ${features.SibSp}
   `)
}
</script>

<template>
<div class='container mx-auto mt-4'>
<div>
   <select class="select select-bordered w-full max-w-xs mb-4" v-model='features.Sex'>
     <option disabled selected>性別を教えてください</option>
     <option>男性</option>
     <option>女性</option>
   </select>
   <br>
   <select class="select select-bordered mb-4" v-model='features.Pclass'>
     <option disabled selected>階級は？</option>
     <option>上層クラス（お金持ち）</option>
     <option>中級クラス（一般階級）</option>
     <option>下層クラス（労働階級）</option>
   </select>
   <br>
   <select class="select select-bordered mb-4" v-model='features.Age'>
   <option diabled selected>年齢は？</option>
   <option v-for='i in [...Array(121).keys()]'>{{i}}</option>
   </select>
   <select class="select select-bordered mb-4 ml-4" v-model='features.Parch'>
   <option diabled selected>親・子の同伴者は？</option>
   <option v-for='i in [...Array(11).keys()]'>{{i}}</option>
   </select>
   <select class="select select-bordered mb-4 ml-4" v-model='features.SibSp'>
   <option diabled selected>兄弟姉妹の同伴者は？</option>
   <option v-for='i in [...Array(11).keys()]'>{{i}}</option>
   </select>
</div>
   <button class="btn btn-primary" v-on:click='displayOutput'>結果を出力</button>
 </div>
</template>

