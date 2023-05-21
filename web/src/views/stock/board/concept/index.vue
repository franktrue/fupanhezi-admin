<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">概念板块</template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @boardCons="boardCons"
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
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="fetchLatest" :loading="loading"><i class="el-icon-refresh" /> 同步数据</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-drawer :visible.sync="drawer" :size="700">
      <div slot="title">
        <span>成分股列表</span>
        <el-tag size="small" style="margin-left: 10px">{{ boardRow.name }}</el-tag>
      </div>
      <board-map
        style="margin-top: 80px; margin-left: 10px"
        :boardRow="boardRow"
      >
      </board-map>
    </el-drawer>
  </d2-container>
</template>

<script>
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData } from './api' // 查询添加修改删除的http请求接口
import BoardMap from '@/views/stock/board/map'
export default {
  name: 'stockBoardConcept',
  components: { BoardMap },
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    return {
      loading: false,
      drawer: false,
      boardRow: {}
    }
  },
  methods: {
    // 获取最新概念
    fetchLatest() {
      const that = this
      this.$confirm('是否确认更新概念信息?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return FetchData().then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        })
      })
    },
    boardCons (scope) {
      this.drawer = true
      this.boardRow = scope.row
      this.boardRow.type = 'concept'
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
