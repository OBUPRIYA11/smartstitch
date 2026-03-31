import nodemailer from 'nodemailer';

export async function sendOrderEmail({ host, port, user, pass, to, subject, text }) {
  const transporter = nodemailer.createTransport({
    host,
    port,
    secure: false,
    auth: { user, pass },
  });

  return transporter.sendMail({
    from: user,
    to,
    subject,
    text,
  });
}

if (process.argv[1] === new URL(import.meta.url).pathname) {
  const payload = JSON.parse(process.argv[2] || '{}');
  sendOrderEmail(payload)
    .then(() => console.log('sent'))
    .catch((err) => {
      console.error(err.message);
      process.exit(1);
    });
}
