<template>
  <div class="qna">
    <div>
      <span>{{ title }}</span>
      <a v-if="!isMypage" href="#" @click.prevent="openQnARegister">등록하기</a>
      <div v-else>
        <label><input type="radio" name="answerType" checked>&nbsp;전체</label>
        <label><input type="radio" name="answerType">&nbsp;답변</label>
        <label><input type="radio" name="answerType">&nbsp;미답변</label>
      </div>
    </div>
    <QnARegister v-bind:id="this.id" v-if="showQnA"></QnARegister>
    <table>
      <colgroup>
        <col v-if="!isMypage" width="15%">
        <col width="15%">
        <col>
        <col width="15%">
        <col width="15%">
      </colgroup>
      <thead>
        <tr>
          <th v-if="!isMypage">분류</th>
          <th v-if="!isMypage">처리상태</th>
          <th v-if="isMypage">답변상태</th>
          <th>내용</th>
          <th>작성자</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="QnA in qnaList">
          <tr @click.prevent="togleAnswer(QnA)" :key="QnA">
            <td v-if="!isMypage">{{ QnA.questionType }}</td>
            <td><span>{{ QnA.isFinished ? '답변 완료' : '답변 대기' }}</span></td>
            <td><p class="scret">{{ QnA.content }}</p></td>
            <td>{{ QnA.writer }}</td>
            <td>{{ QnA.createdAt }}</td>
          </tr>
          <tr class="answer" :class="QnA.answer.isShow" v-if="QnA.answer" :key="QnA.answer">
            <td v-if="!isMypage"></td>
            <td></td>
            <td><p class="scret">{{ QnA.answer.content }}</p></td>
            <td>{{ QnA.answer.writer }}</td>
            <td>{{ QnA.answer.createdAt }}</td>
          </tr>
        </template>
      </tbody>
    </table>
    <a-pagination class="pagination" :default-current="this.page" :total="this.totalCount" :current="this.nowPage" />
    <!-- <Pagenation v-bind="{page:page, totalPage:totalPage}"></Pagenation> -->
  </div>
</template>

<script>
// import axios from 'axios'
// import { VueAgile } from 'vue-agile'
// import mockup from '@/Data/DetailOption.json'
// import Pagenation from '@/service/Components/Pagenation'
import QnARegister from '@/service/Detail/QnARegister'
import { EventBus } from '@/service/util/event-bus'

const limit = 5

export default {
  updated () {
    EventBus.$emit('crrent-page', this.nowPage)
  },
  props: {
    title: String,
    isMypage: Boolean,
    id: Number,
    qnaList: Array,
    totalCount: Number,
    page: Number
  },
  data () {
    return {
      showQnA: false,
      nowPage: 1
    }
  },
  computed: {
    totalPages () {
      const calPage = this.totalCount / limit
      return this.totalCount % limit === 0 ? calPage : calPage + 1
    }
  },
  components: {
    // Pagenation,
    QnARegister
  },
  methods: {
    togleAnswer (answer) {
      answer.answerShow = !answer.answerShow
    },
    openQnARegister () {
      // eslint-disable-next-line no-return-assign
      return this.showQnA = !this.showQnA
    }
  }
}
</script>

<style lang="scss" scoped>
.qna {
  display: flex;
  flex-wrap: wrap;

  div:first-child {
    display: flex;
    width: 100%;
    justify-content: space-between;
    font-size: 2em;
    color: black;
    padding-bottom: 10px;

    span {
      font-weight: 600;
    }
    a {
      color: #000;
    }

    label {
      margin-left: 15px;
      input {
          width: 15px;
          height: 15px;
      }
    }
  }

  table {
    width: 100%;
    border-collapse: 0;
    border-top: 1px solid #000;
    font-size: 18px;
    thead {
      border-bottom: 1px solid #CCC;
      text-align: center;
      th {
        height: 60px;
      }
    }
    tbody {
      tr {
        border-bottom: 1px solid #F1F1F1;
        td {
          text-align: center;
          height: 50px;
          color: #000;
          span {
            display: inline-block;
            border: 1px solid #CCC;
            font-size: 14px;
            color: #999;
            padding: 3px 13px;
            border-radius: 15px;
          }
          p {
            margin: 0;
            text-align: left;
          }
        }
        &.answer td {
          background: #F6F6F6;
          color: #999;
        }
      }
    }
  }

  .pagination {
    margin-top: 30px;
  }
}
</style>
