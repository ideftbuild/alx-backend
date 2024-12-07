#!/usr/bin/node
import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue();

describe('createPushNotificationJobs', () => {
  before(() => {
    queue.testMode.enter();
  });

  it('display a error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('hello', queue))
      .to.throw(Error, 'Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {

    const jobs = [
      { phoneNumber: '123456789', message: 'Notification 1' },
      { phoneNumber: '234567891', message: 'Notification 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs).to.have.lengthOf(2);
    expect(queue.testMode.jobs[0].data.phoneNumber).to.equal(jobs[0].phoneNumber);
    expect(queue.testMode.jobs[0].data.message).to.equal(jobs[0].message);

    expect(queue.testMode.jobs[1].data.phoneNumber).to.equal(jobs[1].phoneNumber);
    expect(queue.testMode.jobs[1].data.message).to.equal(jobs[1].message);
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });
});
