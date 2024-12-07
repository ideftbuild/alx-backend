#!/usr/bin/node
import redis from 'redis';
import { promisify } from 'util';
import express from 'express';
import kue from 'kue';

const client = redis.createClient();
let reservationEnabled = true;

const reserveSeat = (number) => {
  client.set('available_seats', number, (err, reply) => {
    if (err) {
      console.log('Error setting seats in Redis:', err.message);
    } else {
      console.log(reply);
    }
  });
};

const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);
  return getAsync('available_seats');
};

reserveSeat(50);

const app = express();
const queue = kue.createQueue();

app.get('/available_seats', async (req, res) => {
  res.json({ numberOfAvailableSeats: await getCurrentAvailableSeats() });
});

app.get('/reserve_seat', async (req, res) => {
  const currentAvailableSeats = await getCurrentAvailableSeats();

  if (!reservationEnabled || currentAvailableSeats <= 0) {
    reservationEnabled = false;
    res.json({ status: 'Reservation are blocked' });
  } else {
    const job = queue.create('reserve_seat');
    job.save((err) => {
      if (err) {
        res.json({ status: 'Reservation failed' });
      } else {
        res.json({ status: 'Reservation in process' });
      }
    });

    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (err) => {
      console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    });
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    reserveSeat(currentAvailableSeats - 1);

    currentAvailableSeats = await getCurrentAvailableSeats();
    if (Number(currentAvailableSeats) === 0) {
      reservationEnabled = false;
    }

    return done();
  });
});

app.listen(1245);
