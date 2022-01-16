<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>products</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.product-modal>
          Add product
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Price</th>
              <th scope="col">User</th>
              <th scope="col">Quantity</th>
              <th scope="col">Tags</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in products" :key="index">
              <td>{{ product.name }}</td>
              <td>{{ product.price }}</td>
              <td>{{ product.user }}</td>
              <td>{{ product.quantity }}</td>
              <td>{{ product.tags }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.product-update-modal
                          @click="editProduct(product)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteProduct(product)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addProductModal"
            id="product-modal"
            name="Add a new product"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addProductForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-user-group"
                      label="User:"
                      label-for="form-user-input">
            <b-form-input id="form-user-input"
                          type="text"
                          v-model="addProductForm.user"
                          required
                          placeholder="Enter user">
            </b-form-input>
          </b-form-group>
                  <b-form-group id="form-user-group"
                      label="Quantity:"
                      label-for="form-user-input">
            <b-form-input id="form-user-input"
                          type="text"
                          v-model="addProductForm.quantity"
                          required
                          placeholder="Enter user">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-user-group"
                      label="Tags:"
                      label-for="form-user-input">
            <b-form-input id="form-user-input"
                          type="text"
                          v-model="addProductForm.tags"
                          required
                          placeholder="Enter user">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editProductModal"
            id="product-update-modal"
            name="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-name-edit-group"
                    label="Title:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-user-edit-group"
                      label="User:"
                      label-for="form-user-edit-input">
            <b-form-input id="form-user-edit-input"
                          type="text"
                          v-model="editForm.user"
                          required
                          placeholder="Enter user">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-user-edit-group"
                      label="Quantity:"
                      label-for="form-user-edit-input">
            <b-form-input id="form-user-edit-input"
                          type="text"
                          v-model="editForm.quantity"
                          required
                          placeholder="Enter quantity">
            </b-form-input>
          </b-form-group>
                  <b-form-group id="form-user-edit-group"
                      label="Tags:"
                      label-for="form-user-edit-input">
            <b-form-input id="form-user-edit-input"
                          type="text"
                          v-model="editForm.tags"
                          required
                          placeholder="Enter user">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      products: [],
      addProductForm: {
        id: '',
        name: '',
        user: '',
        quantity: 0,
        tags: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        user: '',
        quantity: 0,
        tags: '',
      },
    };
  },
  components: { // TODO change all "Product" to "product"
    alert: Alert,
  },
  methods: {
    getProducts() {
      const path = 'http://127.0.0.1:5000/products';
      axios.get(path)
        .then((res) => {
          this.products = res.data.products;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addProduct(payload) {
      const path = 'http://127.0.0.1:5000/products';
      axios.post(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'product added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getProducts();
        });
    },
    initForm() {
      this.addProductForm.name = '';
      this.addProductForm.user = '';
      this.addProductForm.id = '';
      this.addProductForm.quantity = '';
      this.addProductForm.tags = '';

      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.user = '';
      this.editForm.quantity = '';
      this.editForm.tags = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      const payload = {
        name: this.addProductForm.name,
        user: this.addProductForm.user,
        tags: this.addProductForm.tags,
        quantity: this.addProductForm.quantity,
      };
      this.addProduct(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      this.initForm();
    },
    editProduct(product) {
      this.editForm = product;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      const payload = {
        name: this.editForm.name,
        user: this.editForm.user,
        tags: this.editForm.tags,
        quantity: this.editForm.quantity,
      };
      this.updateProduct(payload, this.editForm.id);
    },
    updateProduct(payload, ProductID) {
      const path = `http://127.0.0.1:5000/products/${ProductID}`;
      axios.put(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'product updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getProducts();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      this.initForm();
      this.getProducts(); // why?
    },
    removeProduct(ProductID) {
      const path = `http://127.0.0.1:5000/products/${ProductID}`;
      axios.delete(path)
        .then(() => {
          this.getProducts();
          this.message = 'product removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getProducts();
        });
    },
    onDeleteProduct(product) {
      this.removeProduct(product.id);
    },
  },
  generateRandomProducts() {
    // TODO request backend to generate random products, names and tag-sets
  },
  created() {
    this.getProducts();
  },
};
</script>
