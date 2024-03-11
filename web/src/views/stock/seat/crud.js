export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
        tableType: "vxe-table",
        rowKey: true, // 必须设置，true or false
        rowId: "id",
        height: "100%", // 表格高度100%, 使用toolbar必须设置
        highlightCurrentRow: false
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
      // custom: [{
      //   text: '关联营业部',
      //   type: 'success',
      //   size: 'small',
      //   icon: 'el-icon-folder',
      //   emit: 'seatOffice'
      // }]
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
      },
      // {
      //   title: '简称',
      //   key: 'short_name',
      //   sortable: true,
      //   search: {
      //     disabled: false,
      //     component: {
      //       props: {
      //         clearable: true
      //       }
      //     }
      //   },
      //   minWidth: 180,
      //   type: 'input',
      //   form: {
      //     component: {
      //       props: {
      //         clearable: true
      //       },
      //       placeholder: '请输入简称'
      //     }
      //   }
      // },
      {
        title: '关联营业部',
        key: 'offices',
        sortable: false,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        minWidth: 180,
        type: 'textarea',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '关联营业部必填项' }
          ],
          component: {
            placeholder: '请输入内容',
            showWordLimit: true,
            maxlength: '1000',
            props: {
              type: 'textarea'
            }
          },
          helper: "请使用“,”隔开"
        }
      }
    ].concat(vm.commonEndColumns({
      description: {
        showTable: true
      }
    }))
  }
}
