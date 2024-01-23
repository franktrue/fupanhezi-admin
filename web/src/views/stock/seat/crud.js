export const crudOptions = (vm) => {
  return {
    pagination: false,
    pageOptions: {
      compact: true
    },
    options: {
      rowKey: true,
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
      // defaultExpandAll: true,
      // expandAll: true,
      treeConfig: {
        transform: true,
        rowField: 'id',
        parentField: 'parent',
        expandAll: true,
        hasChild: 'hasChild',
        lazy: true,
        loadMethod: vm.loadContentMethod
      }
    },
    rowHandle: {
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      width: 280,
      fixed: 'right',
      custom: [{
        text: '关联营业部',
        type: 'success',
        size: 'small',
        icon: 'el-icon-folder',
        emit: 'seatOffice'
      }]

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 80
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        show: false,
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '席位名称',
        key: 'name',
        sortable: true,
        treeNode: true, // 设置为树形列
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        minWidth: 180,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '席位名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入席位名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }

        }
      }
    ].concat(vm.commonEndColumns())
  }
}
