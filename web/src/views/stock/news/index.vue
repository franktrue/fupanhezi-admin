<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">消息面</template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @newsTag="newsTag"
    >
      <!-- 自动绑定参数与事件 -->
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="dialogFormVisible = true"><i class="el-icon-refresh" /> 同步数据</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-drawer :visible.sync="drawer" :size="1000">
      <div slot="title">
        <span>题材标签</span>
        <el-tag size="small" style="margin-left: 10px">{{ subjectRow.title }}</el-tag>
      </div>
      <news-tags style="margin-top: 80px; margin-left: 10px" :subjectRow="subjectRow">
      </news-tags>
    </el-drawer>
  </d2-container>
</template>

<script>
import dayjs from 'dayjs'
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData } from './api' // 查询添加修改删除的http请求接口
import NewsTags from '@/views/stock/news/tag'
export default {
  name: 'stockNews',
  components: { NewsTags },
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    const today = dayjs().format('YYYY-MM-DD')
    return {
      dialogFormVisible: false,
      loading: false,
      fetchForm: {
        trade_date: today,
      },
      fetchFormRules: {
        trade_date: [
          { required: true, message: '必填项' }
        ]
      },
      drawer: false,
      subjectRow: {}
    }
  },
  methods: {
    fetchDataSubmit() {
      const that = this
      that.$refs.fetchForm.validate((valid) => {
        if (valid) {
          that.loading = true
          FetchData(that.fetchForm).then((res) => {
            that.dialogFormVisible = false
            that.loading = false
            that.$message.success('操作成功')
            that.handleSearch()
          }).catch(e => {
            that.loading = false
          })
        } else {
          that.$message.error('表单校验失败，请检查')
        }
      })
    },
    newsTag (scope) {
      this.drawer = true
      this.subjectRow = scope.row
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return GetList(query)
    }, // 数据请求
    addRequest (row) {
      return AddObj(row)
    }, // 添加请求
    updateRequest (row) {
      return UpdateObj(row)
    }, // 修改请求
    delRequest (row) {
      return DelObj(row.id)
    } // 删除请求
  }
}
</script>
