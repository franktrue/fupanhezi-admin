export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      border: false
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 140,
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
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      appendToBody: true, // 子表格必须 否则弹出对话框无法显示最顶层
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [
      {
        title: '股票代码',
        key: 'stock_code',
        width: 100,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '股票代码必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入股票代码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '股票名称',
        key: 'stock_name',
        width: 100,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '股票名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入股票名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '题材解析',
        key: 'brief',
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入解析',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
    ]
  }
}
