#!/usr/bin/node
import kue from 'kue';

const sendNotification = (phoneNumber, message, job, done) => {
  const blackListed = ['4153518780', '4153518781'];
  job.progress(0, 100);
  // console.log('phoneNumber', phoneNumber);
  if (blackListed.includes(phoneNumber)) {
    return done(new Error(`phone number ${phoneNumber} is blacklisted`));
  }
  job.progress(50, 100);
  // console.log('progress:', job.progress.);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  return done();
};

const queue = kue.createQueue();

queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
