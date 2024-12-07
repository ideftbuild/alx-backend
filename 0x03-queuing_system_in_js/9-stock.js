#!/usr/bin/node
import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
];

const getItemById = (id) => listProducts.find((obj) => (obj.id === id));

const client = redis.createClient();

const reserveStockById = (itemId, stock) => {
  const key = `item.${itemId}`;
  client.set(key, stock, (err, reply) => {
    if (err) {
      console.error('Error setting stock in Redis:', err.message);
    } else {
      console.log(`Stock for item ${itemId} set to ${stock}: ${reply}`);
    }
  });
};

const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  return getAsync(itemId);
};

const app = express();

app.get('/list_products', (req, res) => {
  const products = listProducts.map(({
    id,
    name,
    price,
    stock,
  }) => ({
    id,
    name,
    price,
    initialAvailableQuantity: stock,
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  try {
    const currentStock = await getCurrentReservedStockById(`item.${itemId}`);
    const currentQuantity = currentStock !== null ? parseInt(currentStock, 10) : product.stock;

    return res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity,
    });
  } catch (err) {
    return res.status(500).json({ status: 'Error getting stock' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }
  try {
    const currentStock = await getCurrentReservedStockById(`item.${itemId}`);
    const currentQuantity = currentStock !== null ? parseInt(currentStock, 10) : product.stock;

    if (currentQuantity < 1) {
      return res.json({ status: 'Not enough stock available', itemId });
    }

    reserveStockById(itemId, currentQuantity - 1);
    return res.json({ status: 'Reservation confirmed', itemId });
  } catch (err) {
    return res.status(500).json({ status: 'Error reserving stock' });
  }
});

app.listen(1245);
