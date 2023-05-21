export const crudOptions = vm => {
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
          width: 240,
          view: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Retrieve");
              }
          },
          edit: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Update");
              }
          },
          remove: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Delete");
              }
          },
          custom: [
            {
              thin: true,
              text: '成分股',
              size: 'small',
              type: 'success',
              icon: 'el-icon-folder',
              show () {
                return vm.hasPermissions('Fetch')
              },
              emit: 'boardCons'
            }
          ]
      },
      indexRow: false,
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "35%"
      },
      indexRow: { // 或者直接传true,不显示title，不居中
        title: '序号',
        align: 'center',
        width: 60
      },
      columns: [
        {
          title: '行业代码',
          key: 'code',
          width: 140,
          search: {
            component: {
              props: {
                clearable: true
              }
            }
          },
          form: {
            component: {
              props: {
                clearable: true
              }
            },
            rules: [{ required: true, message: '行业代码必填' }]
          }
        },
        {
          title: '行业名称',
          search: true,
          key: 'name',
          search: {
            component: {
              props: {
                clearable: true
              }
            }
          },
          form: {
            component: {

              props: {
                clearable: true
              }
            },
            rules: [{ required: true, message: '行业名称必填' }]
          }
        },
      ]
  };
};
