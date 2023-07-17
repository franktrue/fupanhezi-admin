<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">概念板块</template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @boardSub="boardSub"
      @boardCons="boardCons"
      @boardHistory="boardHistory"
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
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="dialogFormVisible = true"><i class="el-icon-data-line" /> 同步指数数据</el-button>
          <el-button size="small" type="danger" v-permission="'Fetch'" @click="delCache"><i class="el-icon-trash" /> 清除缓存</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-drawer :visible.sync="drawerSub" :size="700">
      <div slot="title">
        <span>二级题材</span>
        <el-tag size="small" style="margin-left: 10px">{{ boardRow.name }}</el-tag>
      </div>
      <board-sub
        style="margin-top: 80px; margin-left: 10px"
        :boardRow="boardRow"
      >
      </board-sub>
    </el-drawer>
    <el-drawer :visible.sync="drawerCons" :size="700">
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
    <el-drawer :visible.sync="drawerHistory" :size="900">
      <div slot="title">
        <span>指数日频率列表</span>
        <el-tag size="small" style="margin-left: 10px">{{ boardRow.name }}</el-tag>
      </div>
      <board-history
        style="margin-top: 80px; margin-left: 10px"
        :boardRow="boardRow"
      >
      </board-history>
    </el-drawer>
    <el-dialog
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <template slot="title">
        同步数据 <small>会更新替换指定日期的指数行情数据</small>
      </template>
      <el-form :model="fetchForm" ref="fetchForm" :rules="fetchFormRules" :inline="true">
        <el-form-item label="交易日" prop="trade_date">
          <el-date-picker
            v-model="fetchForm.trade_date"
            value-format="yyyy-MM-dd"
            :clearable="false"
            type="date"
            placeholder="选择日期">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="fetchDataSubmit" :loading="loading">确定</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import dayjs from 'dayjs'
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData } from './api' // 查询添加修改删除的http请求接口
import { FetchData as FetchHistroy} from '../history/api'
import { DeleteCache } from '@/views/stock/tradeDate/api'
import BoardSub from '@/views/stock/board/sub'
import BoardMap from '@/views/stock/board/map'
import BoardHistory from '@/views/stock/board/history'
export default {
  name: 'stockBoardConcept',
  components: { BoardSub, BoardMap, BoardHistory },
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
      drawerSub: false,
      drawerCons: false,
      drawerHistory: false,
      boardRow: {}
    }
  },
  methods: {
    // 获取最新概念
    fetchLatest() {
      const that = this
      this.$confirm('是否确认更新概念信息?会异步更新对应成分股', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return FetchData().then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        }).catch(e => {
          that.loading = false
        })
      })
    },
    delCache() {
      const that = this
      this.$confirm('确认清除移动端缓存吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return DeleteCache({prefix: "cache:fupanhezi:stockBoardMap:"}).then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        }).catch(e => {
          that.loading = false
        })
      })
    },
    fetchDataSubmit() {
      const that = this
      that.$refs.fetchForm.validate((valid) => {
        if (valid) {
          that.loading = true
          FetchHistroy(that.fetchForm).then((res) => {
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
    boardSub (scope) {
      this.drawerSub = true
      this.boardRow = scope.row
      this.boardRow.type = 'concept'
    },
    boardCons (scope) {
      this.drawerCons = true
      this.boardRow = scope.row
      this.boardRow.type = 'concept'
    },
    boardHistory (scope) {
      this.drawerHistory = true
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
