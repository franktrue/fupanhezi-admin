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
        title: 'ID',
        key: 'id',
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '可用商品',
        key: 'goods_id',
        type: 'select',
        dict: {
          url(dict,{form,component}){
            return '/api/order/goods/'
          },
          value:'id', // value的属性名
          label:'name', // label的属性名
          cache: false,
          onReady:(data,dict,options)=>{
            data.unshift({
              "id": 0,
              "name": "不限商品"
            })
            vm.optionData = data
            vm.formOption = options
          }
        },
        show: false,
        form: {
          value: 0,
          disabled: false,
          component: {
            props: {
              clearable: false
            },
            placeholder: '请输入商品ID'
          },
        }
      },
      {
        title: '商品名称',
        key: 'goods_name',
        type: 'input',
        form: {
          component: {
            show: false
          }
        },
      },
      {
        title: '代理ID',
        key: 'agent_id',
        type: 'input',
        form: {
          value: 0,
          component: {
            props: {
              clearable: false
            },
            placeholder: '请输入代理ID，为0表示不代理'
          },
          helper: "代理分享后，用户将自动获取代理优惠券"
        }
      },
      {
        title: '代理名称',
        key: 'agent_name',
        type: 'input',
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '说明',
        key: 'description',
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入说明',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '是否下架',
        key: 'status',
        type: 'dict-switch',
        dict: {
          data: vm.dictionary('button_whether_number')
        },
        form: {
          value: 0,
          component: {
            props: {
              clearable: true
            }
          },
          helper: "下架后不可用"
        }
      }
    ]
  }
}
